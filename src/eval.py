"""Model evaluation orchestration and leaderboard display.

Optional reference — the workshop notebooks compute metrics inline.
"""

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

from src.metrics import map_at_k, ndcg_at_k, recall_at_k


def evaluate_model(
    recommender,
    train_matrix: csr_matrix,
    test_df: pd.DataFrame,
    k: int = 10,
) -> dict[str, float]:
    """Run a recommender on all test users and compute metrics.

    Parameters
    ----------
    recommender
        Any object with a ``.recommend(user_ids, train_matrix, k)``
        method that returns an (n_users, k) array of item IDs.
    train_matrix : csr_matrix, shape (n_users, n_items)
    test_df : pd.DataFrame
        Must have columns: user_id, item_id (one row per user).
    k : int

    Returns
    -------
    dict with keys: recall@{k}, ndcg@{k}, map@{k}
    """
    user_ids = test_df["user_id"].values
    test_items = test_df["item_id"].values

    ranked_lists = recommender.recommend(user_ids, train_matrix, k=k)

    return {
        f"recall@{k}": recall_at_k(ranked_lists, test_items, k),
        f"ndcg@{k}": ndcg_at_k(ranked_lists, test_items, k),
        f"map@{k}": map_at_k(ranked_lists, test_items, k),
    }


def print_leaderboard(results: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Pretty-print a model-comparison leaderboard.

    Parameters
    ----------
    results : dict[str, dict[str, float]]
        Outer key = model name, inner dict = metric name -> value.

    Returns
    -------
    pd.DataFrame
        Leaderboard sorted by NDCG@10 descending.
    """
    df = pd.DataFrame(results).T
    # Sort by ndcg column (first column containing "ndcg")
    ndcg_col = [c for c in df.columns if "ndcg" in c.lower()][0]
    df = df.sort_values(ndcg_col, ascending=False)
    df.index.name = "model"

    # Format as percentages
    styled = df.style.format("{:.4f}").highlight_max(axis=0, color="#d4edda")
    return styled
