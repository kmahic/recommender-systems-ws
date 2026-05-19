"""Item-item collaborative filtering via cosine similarity."""

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity


class ItemItemRecommender:
    """Nearest-neighbour item-item recommender.

    Computes cosine similarity between item interaction vectors, then
    scores candidate items for a user by aggregating similarities from
    the user's history.
    """

    def __init__(self) -> None:
        self.similarity: np.ndarray | None = None

    def fit(self, train_matrix: csr_matrix) -> "ItemItemRecommender":
        """Compute item-item cosine similarity.

        Parameters
        ----------
        train_matrix : csr_matrix, shape (n_users, n_items)
            Binary interaction matrix.
        """
        # Transpose so rows = items, columns = users
        item_user = train_matrix.T  # (n_items, n_users)
        self.similarity = cosine_similarity(item_user, dense_output=True)
        # Zero out self-similarity to avoid recommending the same item
        np.fill_diagonal(self.similarity, 0.0)
        return self

    def recommend(
        self,
        user_ids: np.ndarray,
        train_matrix: csr_matrix,
        k: int = 10,
    ) -> np.ndarray:
        """Recommend top-K items for each user.

        For each user, score every item by the sum of similarities to
        items the user already interacted with. Exclude seen items.

        Parameters
        ----------
        user_ids : np.ndarray, shape (n,)
        train_matrix : csr_matrix
        k : int

        Returns
        -------
        np.ndarray, shape (n, k)
            Recommended item IDs per user.
        """
        assert self.similarity is not None, "Call .fit() first"
        results = np.zeros((len(user_ids), k), dtype=np.int32)

        # Vectorized: sparse (n_users × n_items) @ dense (n_items × n_items) in one BLAS call
        all_scores = train_matrix[user_ids].dot(self.similarity)  # (n_users, n_items)

        for i, uid in enumerate(user_ids):
            scores = np.asarray(all_scores[i]).flatten() if hasattr(all_scores[i], 'A1') else all_scores[i]
            scores[train_matrix[uid].indices] = -np.inf
            results[i] = np.argsort(-scores)[:k]
        return results
