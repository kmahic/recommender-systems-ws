"""Download MovieLens 25M, sample a workshop-friendly subset, save as parquet."""

import io
import os
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve  # type: ignore

ML25M_URL = "https://files.grouplens.org/datasets/movielens/ml-25m.zip"
DATA_DIR = Path(__file__).resolve().parent
ZIP_PATH = DATA_DIR / "ml-25m.zip"
RAW_DIR = DATA_DIR / "ml-25m"
OUT_DIR = DATA_DIR / "ml-25m-sample"

# Sampling parameters
MIN_USER_INTERACTIONS = 50
MIN_ITEM_INTERACTIONS = 10
TARGET_USERS = 15000
SESSION_GAP_SECONDS = 7200  # 2 hours
SEED = 42
LEA_TARGET_ID = 451  # Lea's guaranteed user_id after reindexing
LEA_NICHE_GENRES = ["Drama", "Film-Noir", "Thriller"]


def _download():
    """Download ML-25M zip if not present."""
    if RAW_DIR.exists():
        print(f"Raw data exists at {RAW_DIR}")
        return
    if not ZIP_PATH.exists():
        print(f"Downloading ML-25M (~250 MB)...")
        urlretrieve(ML25M_URL, ZIP_PATH)
        print("Download complete.")
    print("Extracting...")
    with zipfile.ZipFile(ZIP_PATH) as zf:
        zf.extractall(DATA_DIR)
    print(f"Extracted to {RAW_DIR}")


def _sample_users(ratings: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Keep TARGET_USERS users with >= MIN_USER_INTERACTIONS ratings."""
    user_counts = ratings.groupby("userId").size()
    eligible = user_counts[user_counts >= MIN_USER_INTERACTIONS].index.values
    chosen = rng.choice(eligible, size=min(TARGET_USERS, len(eligible)), replace=False)
    return ratings[ratings["userId"].isin(chosen)].copy()


def _find_lea(df: pd.DataFrame, movies: pd.DataFrame) -> int:
    """Find the best 'Lea' candidate: a niche Drama/Film-Noir/Thriller user.

    Returns the original ML-25M userId of the best candidate.
    """
    # Build genre lookup from raw movies.csv
    genre_exploded = movies.set_index("movieId")["genres"].str.split("|").explode()
    niche_movies = set(
        genre_exploded[genre_exploded.isin(LEA_NICHE_GENRES)].reset_index()["movieId"].unique()
    )

    # Score each user: fraction of their ratings on niche-genre films
    user_counts = df.groupby("userId").size().rename("total")
    niche_mask = df["movieId"].isin(niche_movies)
    niche_counts = df[niche_mask].groupby("userId").size().rename("niche")
    scores = pd.concat([user_counts, niche_counts], axis=1).fillna(0)
    scores["niche_share"] = scores["niche"] / scores["total"]

    # Require enough history for interesting analysis
    scores = scores[scores["total"] >= 100]
    best_user = scores["niche_share"].idxmax()
    print(f"  Lea candidate: userId={best_user}, "
          f"{int(scores.loc[best_user, 'total'])} interactions, "
          f"{scores.loc[best_user, 'niche_share']:.1%} niche share")
    return int(best_user)


def _filter_and_reindex(df: pd.DataFrame, lea_original_id: int | None = None) -> pd.DataFrame:
    """Filter items by min interactions, then 0-index user and item IDs.

    If lea_original_id is given, swap the user mapping so Lea lands at
    user_id=LEA_TARGET_ID (451).
    """
    item_counts = df.groupby("movieId").size()
    keep_items = item_counts[item_counts >= MIN_ITEM_INTERACTIONS].index
    df = df[df["movieId"].isin(keep_items)].copy()

    sorted_users = sorted(df["userId"].unique())
    user_map = {old: new for new, old in enumerate(sorted_users)}

    # Swap Lea into position LEA_TARGET_ID
    if lea_original_id is not None and lea_original_id in user_map:
        lea_natural_idx = user_map[lea_original_id]
        if lea_natural_idx != LEA_TARGET_ID and LEA_TARGET_ID < len(sorted_users):
            # Find who currently sits at LEA_TARGET_ID
            occupant = sorted_users[LEA_TARGET_ID]
            # Swap their positions
            user_map[lea_original_id] = LEA_TARGET_ID
            user_map[occupant] = lea_natural_idx
            print(f"  Planted Lea at user_id={LEA_TARGET_ID} "
                  f"(swapped with original userId={occupant})")

    item_map = {old: new for new, old in enumerate(sorted(df["movieId"].unique()))}
    df["user_id"] = df["userId"].map(user_map)
    df["item_id"] = df["movieId"].map(item_map)
    return df, item_map


def _build_sessions(df: pd.DataFrame) -> pd.DataFrame:
    """Build sessions using gap-based splitting."""
    df = df.sort_values(["user_id", "timestamp"]).reset_index(drop=True)
    time_diff = df.groupby("user_id")["timestamp"].diff().fillna(SESSION_GAP_SECONDS + 1)
    df["new_session"] = (time_diff > SESSION_GAP_SECONDS).astype(int)
    df["session_id"] = df["new_session"].cumsum()
    df["position"] = df.groupby("session_id").cumcount()
    return df[["user_id", "item_id", "session_id", "position", "timestamp"]]


def sample_and_save():
    """Full pipeline: download, sample, save."""
    _download()

    print("Loading ratings...")
    ratings = pd.read_csv(RAW_DIR / "ratings.csv")
    print(f"  Raw: {len(ratings):,} ratings")

    rng = np.random.default_rng(SEED)
    sampled = _sample_users(ratings, rng)

    # Identify the best Lea candidate before reindexing
    movies_raw = pd.read_csv(RAW_DIR / "movies.csv")
    lea_original_id = _find_lea(sampled, movies_raw)
    filtered, item_map = _filter_and_reindex(sampled, lea_original_id)
    print(f"  Sampled: {len(filtered):,} interactions, "
          f"{filtered['user_id'].nunique():,} users, "
          f"{filtered['item_id'].nunique():,} items")

    sessions = _build_sessions(filtered)
    print(f"  Sessions: {sessions['session_id'].nunique():,}")

    # Load and map movie metadata
    movies = movies_raw.copy()
    movies = movies[movies["movieId"].isin(item_map)].copy()
    movies["item_id"] = movies["movieId"].map(item_map)

    # Expand genres to one-hot columns
    all_genres = sorted(set(g for gs in movies["genres"].str.split("|") for g in gs if g != "(no genres listed)"))
    for g in all_genres:
        movies[g] = movies["genres"].str.contains(g, regex=False).astype(int)
    movies = movies.rename(columns={"title": "title"}).drop(columns=["movieId", "genres"])

    # Save
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    interactions = filtered[["user_id", "item_id", "timestamp"]].reset_index(drop=True)
    interactions.to_parquet(OUT_DIR / "interactions.parquet", index=False)
    movies.to_parquet(OUT_DIR / "items.parquet", index=False)
    sessions.to_parquet(OUT_DIR / "sessions.parquet", index=False)
    print(f"\nSaved to {OUT_DIR}/")
    print(f"  interactions.parquet: {len(interactions):,} rows")
    print(f"  items.parquet:       {len(movies):,} rows")
    print(f"  sessions.parquet:    {len(sessions):,} rows")


if __name__ == "__main__":
    sample_and_save()
