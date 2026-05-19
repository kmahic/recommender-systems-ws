"""Fairness and bias analysis utilities."""

import numpy as np
import pandas as pd


def popularity_bias_analysis(recs: np.ndarray, item_pop_counts: np.ndarray,
                             k: int = 10, n_bins: int = 5) -> pd.DataFrame:
    """Compare item popularity distribution in catalogue vs recommendations.

    Returns DataFrame with columns: bin, share_catalogue, share_recommended.
    """
    n_items = len(item_pop_counts)
    sorted_idx = np.argsort(item_pop_counts)
    bin_size = n_items // n_bins

    rows = []
    rec_flat = recs[:, :k].flatten()
    for b in range(n_bins):
        start = b * bin_size
        end = n_items if b == n_bins - 1 else (b + 1) * bin_size
        bin_items = set(sorted_idx[start:end])
        cat_share = len(bin_items) / n_items
        rec_share = np.mean([1 for r in rec_flat if r in bin_items]) / len(rec_flat) if len(rec_flat) > 0 else 0
        label = f"Q{b+1}" if b < n_bins - 1 else f"Q{b+1} (popular)"
        if b == 0:
            label = f"Q{b+1} (niche)"
        rows.append({"bin": label, "share_catalogue": cat_share, "share_recommended": rec_share})
    return pd.DataFrame(rows)


def genre_calibration_score(user_id: int, rec_items: np.ndarray,
                            train_matrix, genre_matrix: np.ndarray,
                            eps: float = 1e-10) -> float:
    """KL-divergence between user's genre distribution and recs' genre distribution.

    Lower = better calibrated (Steck 2018).
    """
    seen = train_matrix[user_id].indices
    if len(seen) == 0 or len(rec_items) == 0:
        return 0.0

    # User's actual genre distribution
    user_genres = genre_matrix[seen].sum(axis=0)
    total = user_genres.sum()
    if total == 0:
        return 0.0
    p = user_genres / total + eps

    # Recommendation genre distribution
    valid_recs = rec_items[rec_items < genre_matrix.shape[0]]
    if len(valid_recs) == 0:
        return 0.0
    rec_genres = genre_matrix[valid_recs].sum(axis=0)
    total_r = rec_genres.sum()
    if total_r == 0:
        return 0.0
    q = rec_genres / total_r + eps

    # KL(p || q)
    return float(np.sum(p * np.log(p / q)))


def group_recall_comparison(recs: np.ndarray, test_items: np.ndarray,
                            train_matrix, item_pop_counts: np.ndarray,
                            k: int = 10) -> pd.DataFrame:
    """Compare Recall@K between niche and mainstream user groups."""
    n_users = recs.shape[0]
    # Compute average popularity of each user's history
    user_avg_pop = np.zeros(n_users)
    for i in range(n_users):
        seen = train_matrix[i].indices
        if len(seen) > 0:
            user_avg_pop[i] = item_pop_counts[seen].mean()

    median_pop = np.median(user_avg_pop[user_avg_pop > 0])
    niche_mask = user_avg_pop <= median_pop
    mainstream_mask = user_avg_pop > median_pop

    rows = []
    for name, mask in [("Niche", niche_mask), ("Mainstream", mainstream_mask)]:
        if mask.sum() == 0:
            continue
        hits = 0
        total = 0
        for i in range(n_users):
            if not mask[i]:
                continue
            if test_items[i] in recs[i, :k]:
                hits += 1
            total += 1
        recall = hits / total if total > 0 else 0
        rows.append({"group": name, "n_users": total, f"recall@{k}": recall})
    return pd.DataFrame(rows)
