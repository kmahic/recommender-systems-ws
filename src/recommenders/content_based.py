"""Content-based recommender using item genre profiles."""

import numpy as np
from scipy.sparse import csr_matrix


class ContentBasedRecommender:
    """Recommend items based on genre-profile similarity.

    Builds a user profile as the (normalised) average of genre vectors
    for items the user has interacted with, then scores all items by
    dot product with the user profile.
    """

    def __init__(self) -> None:
        self.item_profiles: np.ndarray | None = None

    def fit(self, genre_matrix: np.ndarray) -> "ContentBasedRecommender":
        """Store item genre profiles.

        Parameters
        ----------
        genre_matrix : np.ndarray, shape (n_items, n_genres)
            Binary genre indicators per item.
        """
        # L2-normalise each item's genre vector (rows)
        norms = np.linalg.norm(genre_matrix, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        self.item_profiles = genre_matrix / norms
        return self

    @staticmethod
    def build_user_profile(
        user_id: int,
        train_matrix: csr_matrix,
        item_profiles: np.ndarray,
    ) -> np.ndarray:
        """Build a user profile by averaging interacted items' genre vectors.

        Parameters
        ----------
        user_id : int
        train_matrix : csr_matrix, shape (n_users, n_items)
        item_profiles : np.ndarray, shape (n_items, n_genres)

        Returns
        -------
        np.ndarray, shape (n_genres,)
            Normalised user profile vector.
        """
        seen_items = train_matrix[user_id].indices
        if len(seen_items) == 0:
            return np.zeros(item_profiles.shape[1], dtype=np.float32)
        profile = item_profiles[seen_items].mean(axis=0)
        norm = np.linalg.norm(profile)
        if norm > 0:
            profile = profile / norm
        return profile

    def recommend(
        self,
        user_ids: np.ndarray,
        train_matrix: csr_matrix,
        k: int = 10,
    ) -> np.ndarray:
        """Recommend top-K items by dot product with user profile.

        Parameters
        ----------
        user_ids : np.ndarray, shape (n,)
        train_matrix : csr_matrix
        k : int

        Returns
        -------
        np.ndarray, shape (n, k)
        """
        assert self.item_profiles is not None, "Call .fit() first"
        results = np.zeros((len(user_ids), k), dtype=np.int32)

        for i, uid in enumerate(user_ids):
            profile = self.build_user_profile(uid, train_matrix, self.item_profiles)
            scores = self.item_profiles @ profile  # (n_items,)
            scores[train_matrix[uid].indices] = -np.inf
            results[i] = np.argsort(-scores)[:k]
        return results
