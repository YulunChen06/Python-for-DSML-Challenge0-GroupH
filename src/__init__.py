"""Shared MovieLens-20M loading, preprocessing, metrics, and plotting helpers."""

from .load_data import load_movielens, resolve_data_dir, summarize_frames
from .preprocess import build_shared_tables, prepare_movies, prepare_ratings, prepare_tags

__all__ = [
    "build_shared_tables",
    "load_movielens",
    "prepare_movies",
    "prepare_ratings",
    "prepare_tags",
    "resolve_data_dir",
    "summarize_frames",
]

