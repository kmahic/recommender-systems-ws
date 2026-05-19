"""ALS matrix-factorisation recommender (implicit feedback)."""

import numpy as np
from scipy.sparse import csr_matrix

from implicit.als import AlternatingLeastSquares


class ALSRecommender:
    """Thin wrapper around implicit.als.AlternatingLeastSquares.

    Uses the v0.7+ API where .fit() expects a (users x items) CSR
    matrix and .recommend() returns (ids, scores) numpy arrays.
    """

    def __init__(
        self,
        factors: int = 50,
        regularization: float = 0.01,
        iterations: int = 15,
        random_state: int = 42,
    ) -> None:
        self.model = AlternatingLeastSquares(
            factors=factors,
            regularization=regularization,
            iterations=iterations,
            random_state=random_state,
            use_gpu=False,
        )

    def fit(self, train_matrix: csr_matrix, show_progress: bool = True) -> "ALSRecommender":
        """Fit ALS model on implicit interactions.

        Parameters
        ----------
        train_matrix : csr_matrix, shape (n_users, n_items)
            Binary interaction matrix (values are confidence weights).
        show_progress : bool
            Whether to show a progress bar during training.
        """
        self.model.fit(train_matrix, show_progress=show_progress)
        return self

    def recommend(
        self,
        user_ids: np.ndarray,
        train_matrix: csr_matrix,
        k: int = 10,
    ) -> np.ndarray:
        """Recommend top-K items for each user.

        Parameters
        ----------
        user_ids : np.ndarray, shape (n,)
        train_matrix : csr_matrix
            Passed to filter already-liked items.
        k : int

        Returns
        -------
        np.ndarray, shape (n, k)
            Recommended item IDs per user.
        """
        ids, _scores = self.model.recommend(
            user_ids,
            train_matrix[user_ids],
            N=k,
            filter_already_liked_items=True,
        )
        return ids

    @property
    def user_factors(self) -> np.ndarray:
        """User latent factor matrix, shape (n_users, factors)."""
        return self.model.user_factors

    @property
    def item_factors(self) -> np.ndarray:
        """Item latent factor matrix, shape (n_items, factors)."""
        return self.model.item_factors
