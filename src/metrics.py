"""Leader-owned quality checks and dataset-level metrics.

Contributor analyses belong in notebooks/01-03. This module intentionally
does not implement their answers or handoff tables.
"""

from __future__ import annotations

from typing import Mapping

import numpy as np
import pandas as pd


def key_integrity_summary(
    ratings: pd.DataFrame,
    movies: pd.DataFrame,
    tags: pd.DataFrame | None = None,
    genome_scores: pd.DataFrame | None = None,
    genome_tags: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Measure join coverage and orphan identifiers for shared keys."""

    rows: list[dict[str, object]] = []
    movie_ids = set(movies["movieId"].dropna())
    rows.append(
        {
            "check": "ratings.movieId_in_movies",
            "n_records": len(ratings),
            "match_rate": round(ratings["movieId"].isin(movie_ids).mean(), 6)
            if len(ratings)
            else np.nan,
            "orphan_records": int((~ratings["movieId"].isin(movie_ids)).sum()),
        }
    )
    if tags is not None and not tags.empty:
        rows.append(
            {
                "check": "tags.movieId_in_movies",
                "n_records": len(tags),
                "match_rate": round(tags["movieId"].isin(movie_ids).mean(), 6),
                "orphan_records": int((~tags["movieId"].isin(movie_ids)).sum()),
            }
        )
    if genome_scores is not None and not genome_scores.empty:
        rows.append(
            {
                "check": "genome_scores.movieId_in_movies",
                "n_records": len(genome_scores),
                "match_rate": round(
                    genome_scores["movieId"].isin(movie_ids).mean(), 6
                ),
                "orphan_records": int(
                    (~genome_scores["movieId"].isin(movie_ids)).sum()
                ),
            }
        )
        if genome_tags is not None and not genome_tags.empty:
            tag_ids = set(genome_tags["tagId"].dropna())
            rows.append(
                {
                    "check": "genome_scores.tagId_in_genome_tags",
                    "n_records": len(genome_scores),
                    "match_rate": round(
                        genome_scores["tagId"].isin(tag_ids).mean(), 6
                    ),
                    "orphan_records": int(
                        (~genome_scores["tagId"].isin(tag_ids)).sum()
                    ),
                }
            )
    return pd.DataFrame(rows)


def rating_distribution(ratings: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return leader-owned rating counts/percentages and scalar statistics."""

    counts = ratings["rating"].value_counts().sort_index().rename("count").to_frame()
    counts["percentage"] = counts["count"] / counts["count"].sum()
    if ratings["rating"].dropna().empty:
        summary = pd.DataFrame(columns=["metric", "value"])
    else:
        numeric = ratings["rating"].dropna()
        summary = pd.DataFrame(
            {
                "metric": ["count", "mean", "median", "std", "min", "max", "mode"],
                "value": [
                    int(numeric.size),
                    numeric.mean(),
                    numeric.median(),
                    numeric.std(),
                    numeric.min(),
                    numeric.max(),
                    numeric.mode().iloc[0],
                ],
            }
        )
    return counts.reset_index(names="rating"), summary


def runtime_feasibility(
    links: pd.DataFrame | None, movies: pd.DataFrame
) -> dict[str, object]:
    """Document whether runtime is present or needs external metadata."""

    links = links if links is not None else pd.DataFrame()
    runtime_columns = [column for column in links.columns if "runtime" in column.lower()]
    id_columns = [column for column in ["imdbId", "tmdbId"] if column in links.columns]
    parse_rate = float(movies["release_year_parse_ok"].mean()) if len(movies) else np.nan
    if runtime_columns:
        return {
            "runtime_available_in_loaded_files": True,
            "runtime_columns": runtime_columns,
            "external_id_columns": id_columns,
            "release_year_parse_rate": parse_rate,
            "conclusion": "Runtime can be analyzed from the loaded metadata after validating units and missingness.",
        }
    return {
        "runtime_available_in_loaded_files": False,
        "runtime_columns": [],
        "external_id_columns": id_columns,
        "release_year_parse_rate": parse_rate,
        "conclusion": (
            "Runtime is not directly included in the provided MovieLens files. "
            "A reliable runtime trend requires an external metadata source joined "
            "through IMDb/TMDb identifiers; title length is not a valid proxy."
        ),
    }


def data_quality_report(
    frames: Mapping[str, pd.DataFrame],
    ratings: pd.DataFrame,
    movies: pd.DataFrame,
    tags: pd.DataFrame | None = None,
    genome_scores: pd.DataFrame | None = None,
    genome_tags: pd.DataFrame | None = None,
) -> dict[str, pd.DataFrame]:
    """Bundle the leader's file and key-quality checks for export."""

    try:
        from .load_data import summarize_frames
    except ImportError:  # notebooks add src/ directly to sys.path
        from load_data import summarize_frames

    return {
        "file_summary": summarize_frames(frames),
        "key_integrity": key_integrity_summary(
            ratings, movies, tags, genome_scores, genome_tags
        ),
    }
