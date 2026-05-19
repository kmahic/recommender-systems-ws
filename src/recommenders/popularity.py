"""Popularity-based recommender (global item frequency)."""

import numpy as np
from scipy.sparse import csr_matrix


class PopularityRecommender:
    """Recommend the most popular items (by interaction count).

    This is the simplest non-trivial baseline: rank all items by how
    many users interacted with them, then return the top-K that the
    target user hasn't already seen.
    """

    def __init__(self) -> None:
        self.item_scores: np.ndarray | None = None

    def fit(self, train_matrix: csr_matrix) -> "PopularityRecommender":
        """Count interactions per item.

        Parameters
        ----------
        train_matrix : csr_matrix, shape (n_users, n_items)
            Binary interaction matrix.
        """
        # Sum columns -> interaction count per item
        self.item_scores = np.asarray(train_matrix.sum(axis=0)).flatten()
        return self

    def recommend(
        self,
        user_ids: np.ndarray,
        train_matrix: csr_matrix,
        k: int = 10,
    ) -> np.ndarray:
        """Return top-K popular items for each user, excluding seen.

        Parameters
        ----------
        user_ids : np.ndarray, shape (n,)
            User indices to generate recommendations for.
        train_matrix : csr_matrix
            Used to filter already-seen items per user.
        k : int
            Number of items to recommend.

        Returns
        -------
        np.ndarray, shape (n, k)
            Recommended item IDs per user.
        """
        assert self.item_scores is not None, "Call .fit() first"
        global_ranking = np.argsort(-self.item_scores)

        results = np.zeros((len(user_ids), k), dtype=np.int32)
        for i, uid in enumerate(user_ids):
            seen = set(train_matrix[uid].indices)
            recs = [item for item in global_ranking if item not in seen][:k]
            results[i] = recs
        return results
