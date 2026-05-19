"""Train/test splitting strategies for implicit feedback."""

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix


def leave_one_out_split(
    interactions: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Leave-one-out split: hold out each user's last interaction.

    Parameters
    ----------
    interactions : pd.DataFrame
        Must contain columns: user_id, item_id, timestamp.

    Returns
    -------
    train_df, test_df : tuple[pd.DataFrame, pd.DataFrame]
        test_df has exactly one row per user (their most recent
        interaction). train_df has all remaining interactions.
    """
    interactions = interactions.sort_values("timestamp")
    # Last interaction per user -> test
    test_idx = interactions.groupby("user_id")["timestamp"].idxmax()
    test_df = interactions.loc[test_idx].reset_index(drop=True)
    train_df = interactions.drop(test_idx).reset_index(drop=True)
    return train_df, test_df


def build_sparse_matrix(
    df: pd.DataFrame, n_users: int, n_items: int
) -> csr_matrix:
    """Build a sparse (n_users, n_items) binary interaction matrix.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: user_id, item_id (0-indexed).
    n_users, n_items : int
        Dimensions of the output matrix.

    Returns
    -------
    csr_matrix
        Binary interaction matrix of shape (n_users, n_items).
    """
    rows = df["user_id"].values
    cols = df["item_id"].values
    data = np.ones(len(df), dtype=np.float32)
    return csr_matrix((data, (rows, cols)), shape=(n_users, n_items))


def session_train_test_split(
    sessions: pd.DataFrame, interactions: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split sessions: last session per user as test (for users with >=2 sessions).

    Returns
    -------
    train_sessions, test_sessions : tuple[pd.DataFrame, pd.DataFrame]
    """
    session_counts = sessions.groupby("user_id")["session_id"].nunique()
    eligible_users = session_counts[session_counts >= 2].index
    eligible = sessions[sessions["user_id"].isin(eligible_users)]

    # Last session per user
    last_session = (
        eligible.groupby("user_id")
        .agg(last_sid=("session_id", "max"))
        .reset_index()
    )
    test_sids = set(last_session["last_sid"])
    test_sessions = sessions[sessions["session_id"].isin(test_sids)]
    train_sessions = sessions[~sessions["session_id"].isin(test_sids)]
    return train_sessions, test_sessions
