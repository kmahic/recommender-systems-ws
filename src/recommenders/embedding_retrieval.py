"""Embedding-based retrieval using FAISS for approximate nearest neighbor search.

Optional reference — not used in the workshop notebooks.
"""

import numpy as np

try:
    import faiss
except ImportError:
    faiss = None


class EmbeddingRetriever:
    """Wrap a FAISS index for fast inner-product retrieval."""

    def __init__(self, use_approximate: bool = False, n_lists: int = 100, n_probe: int = 10):
        self.use_approximate = use_approximate
        self.n_lists = n_lists
        self.n_probe = n_probe
        self.index = None
        self.item_embeddings = None

    def build_index(self, item_embeddings: np.ndarray):
        """Build FAISS index from item embedding matrix."""
        if faiss is None:
            raise ImportError("faiss-cpu is required: pip install faiss-cpu")
        emb = np.ascontiguousarray(item_embeddings, dtype=np.float32)
        faiss.normalize_L2(emb)
        self.item_embeddings = emb
        dim = emb.shape[1]

        if self.use_approximate:
            quantizer = faiss.IndexFlatIP(dim)
            self.index = faiss.IndexIVFFlat(quantizer, dim, self.n_lists, faiss.METRIC_INNER_PRODUCT)
            self.index.train(emb)
            self.index.add(emb)
            self.index.nprobe = self.n_probe
        else:
            self.index = faiss.IndexFlatIP(dim)
            self.index.add(emb)
        return self

    def retrieve(self, user_embeddings: np.ndarray, k: int = 100):
        """Retrieve top-k items by inner product.

        Returns (ids, scores) arrays of shape (n_queries, k).
        """
        queries = np.ascontiguousarray(user_embeddings, dtype=np.float32)
        faiss.normalize_L2(queries)
        scores, ids = self.index.search(queries, k)
        return ids, scores

    def recommend(self, user_embeddings: np.ndarray, train_matrix,
                  user_ids: np.ndarray, k: int = 10, retrieve_k: int = 200):
        """Recommend top-k unseen items per user."""
        ids, scores = self.retrieve(user_embeddings, k=retrieve_k)
        results = np.zeros((len(user_ids), k), dtype=np.int32)
        for i, uid in enumerate(user_ids):
            seen = set(train_matrix[uid].indices)
            filtered = [item_id for item_id in ids[i] if item_id not in seen]
            results[i] = filtered[:k]
        return results
