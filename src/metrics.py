"""Analysis metrics shared by the leader and contributor notebooks."""

from __future__ import annotations

from itertools import combinations
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
    """Measure join coverage and orphan identifiers for the shared keys."""

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
    if genome_tags is not None and not genome_tags.empty and genome_scores is not None:
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
    """Return rating counts/percentages and scalar descriptive statistics."""

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


def user_activity_summary(user_stats: pd.DataFrame) -> pd.DataFrame:
    quantiles = [0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1]
    if user_stats.empty:
        return pd.DataFrame(columns=["quantile", "rating_count"])
    values = user_stats["rating_count"].quantile(quantiles)
    return pd.DataFrame({"quantile": quantiles, "rating_count": values.values})


def assign_activity_groups(user_stats: pd.DataFrame) -> pd.DataFrame:
    """Assign distribution-based activity groups without arbitrary thresholds."""

    result = user_stats.copy()
    if result.empty:
        result["activity_group"] = pd.Series(dtype="string")
        return result
    percentile = result["rating_count"].rank(method="average", pct=True)
    result["activity_group"] = np.select(
        [percentile <= 0.50, percentile <= 0.90, percentile <= 0.99],
        ["Low (bottom 50%)", "Medium (50-90%)", "High (90-99%)"],
        default="Very high (top 1%)",
    )
    return result


def activity_group_summary(user_stats: pd.DataFrame) -> pd.DataFrame:
    grouped = assign_activity_groups(user_stats)
    if grouped.empty:
        return pd.DataFrame(
            columns=[
                "activity_group",
                "n_users",
                "median_rating_count",
                "mean_avg_rating",
                "median_avg_rating",
                "mean_rating_std",
            ]
        )
    return (
        grouped.groupby("activity_group", sort=False)
        .agg(
            n_users=("userId", "nunique"),
            median_rating_count=("rating_count", "median"),
            mean_avg_rating=("avg_rating", "mean"),
            median_avg_rating=("avg_rating", "median"),
            mean_rating_std=("rating_std", "mean"),
        )
        .reset_index()
    )


def genre_summary(
    exploded_genres: pd.DataFrame, rating_genre_df: pd.DataFrame
) -> pd.DataFrame:
    movie_counts = (
        exploded_genres.groupby("genre", as_index=False)["movieId"]
        .nunique()
        .rename(columns={"movieId": "movie_count"})
    )
    rating_stats = (
        rating_genre_df.groupby("genre", as_index=False)
        .agg(
            rating_count=("rating", "size"),
            avg_rating=("rating", "mean"),
            median_rating=("rating", "median"),
            rating_std=("rating", "std"),
            rating_var=("rating", "var"),
        )
    )
    result = movie_counts.merge(rating_stats, on="genre", how="outer")
    result["movie_count"] = result["movie_count"].fillna(0).astype(int)
    result["rating_count"] = result["rating_count"].fillna(0).astype(int)
    return result.sort_values(["movie_count", "rating_count"], ascending=False).reset_index(
        drop=True
    )


def genre_q1_table(
    movie_stats: pd.DataFrame,
    rating_genre_df: pd.DataFrame,
    exploded_genres: pd.DataFrame,
    *,
    min_movie_ratings: int = 1000,
) -> pd.DataFrame:
    """Answer Q1 with raw and ``rating_count >= min_movie_ratings`` views."""

    scopes: list[tuple[str, pd.DataFrame]] = [("all movies", movie_stats)]
    scopes.append(
        (
            f"movies with >= {min_movie_ratings} ratings",
            movie_stats.loc[movie_stats["rating_count"] >= min_movie_ratings],
        )
    )
    rows: list[pd.DataFrame] = []
    for scope, movies_in_scope in scopes:
        movie_ids = set(movies_in_scope["movieId"])
        scoped_ratings = rating_genre_df.loc[rating_genre_df["movieId"].isin(movie_ids)]
        scoped_genres = exploded_genres.loc[exploded_genres["movieId"].isin(movie_ids)]
        stats = genre_summary(scoped_genres, scoped_ratings)
        if not stats.empty:
            top = stats.sort_values(
                ["avg_rating", "rating_count"], ascending=[False, False]
            ).head(1).copy()
            top.insert(0, "scope", scope)
            rows.append(top)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def ratings_by_year(ratings: pd.DataFrame) -> pd.DataFrame:
    return (
        ratings.dropna(subset=["rating_year"])
        .groupby("rating_year", as_index=False)
        .agg(rating_count=("rating", "size"), avg_rating=("rating", "mean"))
        .sort_values("rating_year")
    )


def release_year_stats(
    ratings: pd.DataFrame, movies: pd.DataFrame, *, min_rating_count: int = 1000
) -> pd.DataFrame:
    merged = ratings.merge(
        movies[["movieId", "release_year"]], on="movieId", how="left"
    ).dropna(subset=["release_year"])
    result = (
        merged.groupby("release_year", as_index=False)
        .agg(
            rating_count=("rating", "size"),
            avg_rating=("rating", "mean"),
            median_rating=("rating", "median"),
        )
        .sort_values("release_year")
    )
    return result.loc[result["rating_count"] >= min_rating_count].reset_index(drop=True)


def decade_summary(
    ratings: pd.DataFrame, movies: pd.DataFrame, exploded_genres: pd.DataFrame
) -> pd.DataFrame:
    movie_frame = movies.dropna(subset=["release_decade"])
    movie_counts = movie_frame.groupby("release_decade").agg(movie_count=("movieId", "nunique"))
    rating_frame = ratings.merge(
        movie_frame[["movieId", "release_decade"]], on="movieId", how="inner"
    )
    rating_counts = rating_frame.groupby("release_decade").agg(
        rating_count=("rating", "size"),
        avg_rating=("rating", "mean"),
        median_rating=("rating", "median"),
        rating_std=("rating", "std"),
    )
    result = movie_counts.join(rating_counts, how="outer").reset_index()
    return result.sort_values("release_decade").reset_index(drop=True)


def genre_pair_stats(
    ratings: pd.DataFrame,
    movies: pd.DataFrame,
    genre_stats: pd.DataFrame,
    *,
    min_movie_count: int = 50,
) -> pd.DataFrame:
    """Compare multi-genre pair averages with the individual genre averages."""

    pair_rows: list[dict[str, object]] = []
    for row in movies[["movieId", "genre_list"]].itertuples(index=False):
        genres = sorted(set(row.genre_list))
        pair_rows.extend(
            {"movieId": row.movieId, "genre_a": a, "genre_b": b, "genre_pair": f"{a} + {b}"}
            for a, b in combinations(genres, 2)
        )
    pairs = pd.DataFrame(pair_rows)
    if pairs.empty:
        return pd.DataFrame()
    pair_ratings = pairs.merge(ratings[["movieId", "rating"]], on="movieId", how="inner")
    result = (
        pair_ratings.groupby(["genre_pair", "genre_a", "genre_b"], as_index=False)
        .agg(
            movie_count=("movieId", "nunique"),
            rating_count=("rating", "size"),
            pair_avg=("rating", "mean"),
            pair_median=("rating", "median"),
            pair_rating_std=("rating", "std"),
        )
    )
    average_by_genre = genre_stats.set_index("genre")["avg_rating"].to_dict()
    result["single_a_avg"] = result["genre_a"].map(average_by_genre)
    result["single_b_avg"] = result["genre_b"].map(average_by_genre)
    result["gain_vs_best_single"] = result["pair_avg"] - result[["single_a_avg", "single_b_avg"]].max(axis=1)
    result["gain_vs_single_mean"] = result["pair_avg"] - result[["single_a_avg", "single_b_avg"]].mean(axis=1)
    return result.loc[result["movie_count"] >= min_movie_count].sort_values(
        ["gain_vs_best_single", "rating_count"], ascending=[False, False]
    ).reset_index(drop=True)


def normalize_tag_key(values: pd.Series) -> pd.Series:
    return (
        values.fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace("-", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
    )


def tag_summary(tags: pd.DataFrame) -> pd.DataFrame:
    if tags.empty or "tag_clean" not in tags.columns:
        return pd.DataFrame(columns=["tag", "application_count", "movie_count", "user_count"])
    usable = tags.loc[~tags["tag_is_empty"]]
    return (
        usable.groupby("tag_clean", as_index=False)
        .agg(
            application_count=("tag_clean", "size"),
            movie_count=("movieId", "nunique"),
            user_count=("userId", "nunique"),
        )
        .rename(columns={"tag_clean": "tag"})
        .sort_values(["application_count", "movie_count"], ascending=False)
        .reset_index(drop=True)
    )


def tag_genome_comparison(
    tags: pd.DataFrame,
    genome_scores: pd.DataFrame,
    genome_tags: pd.DataFrame,
) -> pd.DataFrame:
    """Compare user-tag frequency with relevance on the movies they tagged."""

    if tags.empty or genome_scores.empty or genome_tags.empty:
        return pd.DataFrame(
            columns=[
                "tag",
                "user_application_count",
                "tagged_movie_count",
                "user_tag_user_count",
                "genome_tag_id",
                "matched_movie_count",
                "mean_genome_relevance",
            ]
        )
    usable = tags.loc[~tags["tag_is_empty"]].copy()
    usable["tag_key"] = normalize_tag_key(usable["tag_clean"])
    genome = genome_tags.copy()
    genome["tag_key"] = normalize_tag_key(genome["tag"])
    user_summary = (
        usable.groupby(["tag_clean", "tag_key"], as_index=False)
        .agg(
            user_application_count=("tag_clean", "size"),
            tagged_movie_count=("movieId", "nunique"),
            user_tag_user_count=("userId", "nunique"),
        )
        .rename(columns={"tag_clean": "tag"})
    )
    movie_tag_rows = usable[["tag", "tag_key", "movieId"]].drop_duplicates()
    mapped = movie_tag_rows.merge(
        genome[["tagId", "tag", "tag_key"]].rename(columns={"tag": "genome_tag"}),
        on="tag_key",
        how="inner",
        suffixes=("_user", "_genome"),
    )
    relevance_rows = mapped.merge(
        genome_scores[["movieId", "tagId", "relevance"]],
        on=["movieId", "tagId"],
        how="inner",
    )
    relevance = (
        relevance_rows.groupby(["tag", "tag_key", "tagId"], as_index=False)
        .agg(
            matched_movie_count=("movieId", "nunique"),
            mean_genome_relevance=("relevance", "mean"),
        )
        .rename(columns={"tagId": "genome_tag_id"})
    )
    result = user_summary.merge(relevance, on=["tag", "tag_key"], how="left")
    return result.drop(columns=["tag_key"]).sort_values(
        ["user_application_count", "mean_genome_relevance"], ascending=[False, False]
    ).reset_index(drop=True)


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

