"""Consistent matplotlib figures used by the project notebooks."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_rating_distribution(counts: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(counts["rating"].astype(str), counts["count"], color="#35618d")
    ax.set_title("MovieLens rating distribution")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Number of ratings")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig


def plot_user_activity(user_stats: pd.DataFrame, *, log_scale: bool = False) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    values = user_stats["rating_count"].clip(lower=1)
    ax.hist(values, bins=40, color="#6b8e23", alpha=0.85)
    if log_scale:
        ax.set_xscale("log")
        ax.set_title("Ratings per user (log-scaled x-axis)")
    else:
        ax.set_title("Ratings per user")
    ax.set_xlabel("Number of ratings given")
    ax.set_ylabel("Number of users")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig


def plot_top_genres(genre_stats: pd.DataFrame, *, top_n: int = 10) -> plt.Figure:
    top = genre_stats.nlargest(top_n, "movie_count").sort_values("movie_count")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top["genre"], top["movie_count"], color="#9c6644")
    ax.set_title(f"Top {top_n} genres by movie count")
    ax.set_xlabel("Unique movies")
    ax.set_ylabel("Genre")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    return fig


def plot_genre_rating_boxplot(
    rating_genre_df: pd.DataFrame, genre_stats: pd.DataFrame, *, top_n: int = 5
) -> plt.Figure:
    top_genres = genre_stats.nlargest(top_n, "movie_count")["genre"].tolist()
    values = [
        rating_genre_df.loc[rating_genre_df["genre"].eq(genre), "rating"].dropna()
        for genre in top_genres
    ]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.boxplot(values, patch_artist=True, boxprops={"facecolor": "#d9c2a6"})
    ax.set_xticks(range(1, len(top_genres) + 1))
    ax.set_xticklabels(top_genres, rotation=25, ha="right")
    ax.set_title(f"Rating distributions for the top {top_n} genres by movie count")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Rating")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig


def save_figure(fig: plt.Figure, path: str | Path, *, dpi: int = 150) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    return output_path

