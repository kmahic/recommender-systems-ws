"""Offline evaluation metrics for implicit-feedback recommenders."""

import numpy as np


def recall_at_k(
    ranked_lists: np.ndarray,
    test_items: np.ndarray,
    k: int = 10,
) -> float:
    """Recall@K (hit rate) for leave-one-out evaluation.

    Parameters
    ----------
    ranked_lists : np.ndarray, shape (n_users, >=k)
        Each row is an ordered list of recommended item IDs.
    test_items : np.ndarray, shape (n_users,)
        The held-out ground-truth item ID per user.
    k : int
        Cut-off position.

    Returns
    -------
    float
        Mean Recall@K across all users (equivalent to hit rate when
        there is exactly one relevant item per user).
    """
    top_k = ranked_lists[:, :k]
    hits = np.any(top_k == test_items[:, np.newaxis], axis=1)
    return float(hits.mean())


def ndcg_at_k(
    ranked_lists: np.ndarray,
    test_items: np.ndarray,
    k: int = 10,
) -> float:
    """NDCG@K for leave-one-out evaluation (binary relevance).

    With a single relevant item, NDCG@K = 1 / log2(rank + 1) if the
    item appears at position rank <= K, else 0.

    Parameters
    ----------
    ranked_lists : np.ndarray, shape (n_users, >=k)
    test_items : np.ndarray, shape (n_users,)
    k : int

    Returns
    -------
    float
        Mean NDCG@K across all users.
    """
    top_k = ranked_lists[:, :k]
    # Find rank of the test item (1-indexed); 0 if not in top-K
    match = top_k == test_items[:, np.newaxis]  # (n_users, k)
    # rank position (1-indexed) of the match, or 0 if no match
    ranks = np.where(match.any(axis=1), match.argmax(axis=1) + 1, 0).astype(np.float64)
    ranks_safe = np.where(ranks > 0, ranks, 1.0)  # avoid log2(1)=0 on miss
    ndcg = np.where(ranks > 0, 1.0 / np.log2(ranks_safe + 1), 0.0)
    return float(ndcg.mean())


def map_at_k(
    ranked_lists: np.ndarray,
    test_items: np.ndarray,
    k: int = 10,
) -> float:
    """MAP@K for leave-one-out evaluation (equivalent to MRR).

    With a single relevant item, AP@K = 1/rank if the item appears at
    position rank <= K, else 0. MAP = mean over users.

    Parameters
    ----------
    ranked_lists : np.ndarray, shape (n_users, >=k)
    test_items : np.ndarray, shape (n_users,)
    k : int

    Returns
    -------
    float
        Mean AP@K across all users.
    """
    top_k = ranked_lists[:, :k]
    match = top_k == test_items[:, np.newaxis]
    ranks = np.where(match.any(axis=1), match.argmax(axis=1) + 1, 0).astype(np.float64)
    ranks_safe = np.where(ranks > 0, ranks, 1.0)  # avoid div-by-zero on miss
    ap = np.where(ranks > 0, 1.0 / ranks_safe, 0.0)
    return float(ap.mean())


def coverage(
    ranked_lists: np.ndarray,
    n_items: int,
    k: int = 10,
) -> float:
    """Catalogue coverage: fraction of items appearing in any top-K list."""
    unique_items = set(ranked_lists[:, :k].flatten())
    return len(unique_items) / n_items


def novelty(
    ranked_lists: np.ndarray,
    item_popularity: np.ndarray,
    k: int = 10,
) -> float:
    """Mean self-information of recommended items (higher = more novel).

    Parameters
    ----------
    item_popularity : np.ndarray, shape (n_items,)
        Fraction of users who interacted with each item.
    """
    top_k = ranked_lists[:, :k]
    pop = item_popularity[top_k]
    pop = np.clip(pop, 1e-10, 1.0)
    return float(-np.log2(pop).mean())


def intra_list_similarity(
    ranked_lists: np.ndarray,
    feature_matrix: np.ndarray,
    k: int = 10,
) -> float:
    """Mean pairwise cosine similarity within each user's top-K list.

    Lower = more diverse.
    """
    from sklearn.metrics.pairwise import cosine_similarity
    total = 0.0
    n = len(ranked_lists)
    for recs in ranked_lists[:, :k]:
        vecs = feature_matrix[recs]
        sim = cosine_similarity(vecs)
        # Mean of upper triangle
        mask = np.triu_indices(k, k=1)
        total += sim[mask].mean()
    return total / n
