"""Load the sampled MovieLens 25M workshop dataset."""

from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "ml-25m-sample"

GENRE_COLS = [
    "Drama", "Action", "Adventure", "Animation", "Children", "Comedy", "Crime",
    "Documentary", "Fantasy", "Film-Noir", "Horror", "IMAX",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western",
]


def load_interactions(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load user-item interactions.

    Returns DataFrame with columns: user_id, item_id, timestamp.
    """
    return pd.read_parquet(data_dir / "interactions.parquet")


def load_item_metadata(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load movie metadata including genre binary indicators."""
    return pd.read_parquet(data_dir / "items.parquet")


def load_sessions(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load session data.

    Returns DataFrame with columns: user_id, item_id, session_id, position, timestamp.
    """
    return pd.read_parquet(data_dir / "sessions.parquet")


def get_genre_matrix(items: pd.DataFrame) -> np.ndarray:
    """Extract genre one-hot matrix from item metadata.

    Returns ndarray of shape (n_items, n_genres), float32.
    """
    genre_matrix = items[GENRE_COLS].fillna(0)
    return genre_matrix.values.astype(np.float32)
