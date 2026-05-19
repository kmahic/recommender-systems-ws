"""Session-aware recommender using Markov chain transitions."""

import numpy as np
from scipy.sparse import lil_matrix


class SessionRecommender:
    """First-order Markov chain: P(next item | current item)."""

    def __init__(self, decay: float = 0.8):
        self.decay = decay
        self.transition = None

    def fit(self, sessions_df, n_items: int):
        """Build transition probability matrix from session data."""
        counts = lil_matrix((n_items, n_items), dtype=np.float64)
        df = sessions_df.sort_values(["session_id", "position"])
        prev_item, prev_session = -1, -1
        for _, row in df.iterrows():
            sid = row["session_id"]
            item = row["item_id"]
            if sid == prev_session and prev_item >= 0:
                counts[prev_item, item] += 1
            prev_item, prev_session = item, sid

        csr = counts.tocsr()
        row_sums = np.asarray(csr.sum(axis=1)).flatten()
        row_sums[row_sums == 0] = 1.0
        from scipy.sparse import diags
        self.transition = (diags(1.0 / row_sums) @ csr).toarray()
        return self

    def session_scores(self, context_items: list, n_items: int = None) -> np.ndarray:
        """Compute scores from recent session context with exponential decay."""
        if n_items is None:
            n_items = self.transition.shape[0]
        scores = np.zeros(n_items)
        weight = 1.0
        for item in reversed(context_items[-3:]):
            if 0 <= item < self.transition.shape[0]:
                scores += weight * self.transition[item]
            weight *= self.decay
        return scores

    def recommend_session(self, context_items: list, seen: set,
                          k: int = 10) -> np.ndarray:
        """Recommend top-k items given session context, filtering seen."""
        scores = self.session_scores(context_items)
        for s in seen:
            if 0 <= s < len(scores):
                scores[s] = -np.inf
        return np.argsort(-scores)[:k]
