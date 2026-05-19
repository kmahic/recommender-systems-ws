"""Re-ranking strategies for diversity and business constraints."""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as _cos_sim


def category_constrained_rerank(
    candidates: np.ndarray,
    scores: np.ndarray,
    item_genres: np.ndarray,
    k: int = 10,
    max_per_genre: int = 3,
) -> np.ndarray:
    """Greedy re-ranking with per-genre caps.

    Iterates through candidates in score order and adds an item only if
    none of its genres have exceeded ``max_per_genre`` in the output.

    Parameters
    ----------
    candidates : np.ndarray, shape (n,)
        Item IDs sorted by descending score.
    scores : np.ndarray, shape (n,)
        Corresponding scores.
    item_genres : np.ndarray, shape (n_items, n_genres)
        Binary genre matrix.
    k : int
        Number of items to select.
    max_per_genre : int
        Maximum items per genre in the output.

    Returns
    -------
    np.ndarray, shape (k,)
        Re-ranked item IDs.
    """
    genre_counts = np.zeros(item_genres.shape[1], dtype=int)
    selected: list[int] = []

    for item_id in candidates:
        if len(selected) >= k:
            break
        genres = item_genres[item_id]  # binary vector
        active_genres = np.where(genres > 0)[0]
        # Check if any of this item's genres are over the cap
        if all(genre_counts[g] < max_per_genre for g in active_genres):
            selected.append(int(item_id))
            genre_counts[active_genres] += 1

    # If not enough items passed the constraint, fill from remaining
    if len(selected) < k:
        remaining = [int(c) for c in candidates if c not in selected]
        selected.extend(remaining[: k - len(selected)])

    return np.array(selected[:k], dtype=np.int32)


def mmr_rerank(
    candidates: np.ndarray,
    scores: np.ndarray,
    item_features: np.ndarray,
    k: int = 10,
    lambda_: float = 0.5,
) -> np.ndarray:
    """Maximal Marginal Relevance (MMR) re-ranking.

    Iteratively selects items that balance relevance (score) and
    diversity (dissimilarity to already-selected items), controlled
    by ``lambda_`` (1.0 = pure relevance, 0.0 = pure diversity).

    Parameters
    ----------
    candidates : np.ndarray, shape (n,)
        Candidate item IDs.
    scores : np.ndarray, shape (n,)
        Relevance scores for each candidate.
    item_features : np.ndarray, shape (n_items, n_features)
        Feature vectors for computing similarity (e.g. genre vectors).
    k : int
        Number of items to select.
    lambda_ : float
        Trade-off parameter in [0, 1].

    Returns
    -------
    np.ndarray, shape (k,)
        Re-ranked item IDs.
    """
    # Normalise scores to [0, 1]
    s = scores.astype(np.float64)
    s_min, s_max = s.min(), s.max()
    if s_max > s_min:
        s = (s - s_min) / (s_max - s_min)
    else:
        s = np.ones_like(s)

    # Pre-compute pairwise similarity among candidates
    feats = item_features[candidates]  # (n, n_features)
    sim = _cos_sim(feats)  # (n, n)

    selected_idx: list[int] = []
    remaining = set(range(len(candidates)))

    for _ in range(min(k, len(candidates))):
        best_idx, best_score = -1, -np.inf
        for idx in remaining:
            relevance = s[idx]
            if selected_idx:
                max_sim = max(sim[idx, j] for j in selected_idx)
            else:
                max_sim = 0.0
            mmr_score = lambda_ * relevance - (1 - lambda_) * max_sim
            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = idx
        selected_idx.append(best_idx)
        remaining.discard(best_idx)

    return candidates[selected_idx]
