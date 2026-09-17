"""Shared, reproducible MovieLens preprocessing tables."""

from __future__ import annotations

from typing import Iterable

import pandas as pd


def _require_columns(frame: pd.DataFrame, required: Iterable[str], name: str) -> None:
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"{name} is missing required columns: {missing}")


def _parse_timestamp(values: pd.Series) -> pd.Series:
    """Parse MovieLens epoch-second timestamps with a text fallback."""

    numeric = pd.to_numeric(values, errors="coerce")
    numeric_dates = pd.to_datetime(numeric, unit="s", errors="coerce", utc=True)
    text_dates = pd.to_datetime(values, errors="coerce", utc=True)
    parsed = numeric_dates.fillna(text_dates)
    return parsed.dt.tz_convert(None)


def prepare_ratings(ratings: pd.DataFrame) -> pd.DataFrame:
    """Add normalized rating timestamps and calendar features."""

    _require_columns(ratings, ["userId", "movieId", "rating", "timestamp"], "ratings")
    result = ratings.copy()
    result["userId"] = pd.to_numeric(result["userId"], errors="coerce").astype("Int64")
    result["movieId"] = pd.to_numeric(result["movieId"], errors="coerce").astype("Int64")
    result["rating"] = pd.to_numeric(result["rating"], errors="coerce")
    result["rating_datetime"] = _parse_timestamp(result["timestamp"])
    result["rating_year"] = result["rating_datetime"].dt.year.astype("Int64")
    result["rating_month"] = result["rating_datetime"].dt.month.astype("Int64")
    result["rating_dayofweek"] = result["rating_datetime"].dt.dayofweek.astype("Int64")
    return result


def _parse_genre_list(value: object) -> list[str]:
    if pd.isna(value):
        return []
    text = str(value).strip()
    if not text or text == "(no genres listed)":
        return []
    return [genre.strip() for genre in text.split("|") if genre.strip()]


def prepare_movies(movies: pd.DataFrame) -> pd.DataFrame:
    """Parse release years, clean titles, and create genre features.

    The trailing four-digit year is parsed only when it appears in the final
    parenthesized group.  Parse failures remain visible in
    ``release_year_parse_ok`` instead of being silently discarded.
    """

    _require_columns(movies, ["movieId", "title", "genres"], "movies")
    result = movies.copy()
    result["movieId"] = pd.to_numeric(result["movieId"], errors="coerce").astype("Int64")
    result["title"] = result["title"].fillna("").astype(str)
    result["genres"] = result["genres"].fillna("").astype(str)
    result["release_year"] = pd.to_numeric(
        result["title"].str.extract(r"\((\d{4})\)\s*$", expand=False),
        errors="coerce",
    ).astype("Int64")
    result["release_year_parse_ok"] = result["release_year"].notna()
    result["clean_title"] = result["title"].str.replace(
        r"\s*\(\d{4}\)\s*$", "", regex=True
    ).str.strip()
    result["genre_list"] = result["genres"].map(_parse_genre_list)
    result["genre_count"] = result["genre_list"].map(len).astype("Int64")
    result["is_multigenre"] = result["genre_count"].gt(1)
    result["release_decade"] = ((result["release_year"] // 10) * 10).astype("Int64")
    return result


def prepare_tags(tags: pd.DataFrame) -> pd.DataFrame:
    """Normalize user tags without stemming or semantic merging."""

    _require_columns(tags, ["userId", "movieId", "tag", "timestamp"], "tags")
    result = tags.copy()
    result["userId"] = pd.to_numeric(result["userId"], errors="coerce").astype("Int64")
    result["movieId"] = pd.to_numeric(result["movieId"], errors="coerce").astype("Int64")
    result["tag_clean"] = result["tag"].fillna("").astype(str).str.strip().str.lower()
    result["tag_is_empty"] = result["tag_clean"].eq("")
    result["tag_datetime"] = _parse_timestamp(result["timestamp"])
    result["tag_year"] = result["tag_datetime"].dt.year.astype("Int64")
    return result


def prepare_genome_tags(genome_tags: pd.DataFrame) -> pd.DataFrame:
    _require_columns(genome_tags, ["tagId", "tag"], "genome-tags")
    result = genome_tags.copy()
    result["tagId"] = pd.to_numeric(result["tagId"], errors="coerce").astype("Int64")
    result["tag"] = result["tag"].fillna("").astype(str).str.strip()
    return result


def prepare_genome_scores(genome_scores: pd.DataFrame) -> pd.DataFrame:
    _require_columns(genome_scores, ["movieId", "tagId", "relevance"], "genome-scores")
    result = genome_scores.copy()
    result["movieId"] = pd.to_numeric(result["movieId"], errors="coerce").astype("Int64")
    result["tagId"] = pd.to_numeric(result["tagId"], errors="coerce").astype("Int64")
    result["relevance"] = pd.to_numeric(result["relevance"], errors="coerce")
    return result


def explode_genres(movies: pd.DataFrame) -> pd.DataFrame:
    """Return one row per movie-genre pair.

    Movies with ``(no genres listed)`` are excluded because there is no genre
    category to attribute their ratings to; their count remains visible in the
    movie-level tables.
    """

    columns = ["movieId", "title", "release_year", "release_decade", "genre_list"]
    available = [column for column in columns if column in movies.columns]
    result = movies.loc[movies["genre_list"].map(bool), available].copy()
    result = result.explode("genre_list", ignore_index=True)
    result = result.rename(columns={"genre_list": "genre"})
    result["genre"] = result["genre"].astype(str).str.strip()
    return result[result["genre"].ne("")].reset_index(drop=True)


def _empty_movie_stats() -> pd.DataFrame:
    return pd.DataFrame(
        columns=["movieId", "rating_count", "avg_rating", "rating_std"]
    )


def _empty_user_stats() -> pd.DataFrame:
    return pd.DataFrame(columns=["userId", "rating_count", "avg_rating", "rating_std"])


def build_shared_tables(
    ratings: pd.DataFrame,
    movies: pd.DataFrame,
    tags: pd.DataFrame | None = None,
) -> dict[str, pd.DataFrame]:
    """Build the common tables consumed by all team notebooks."""

    ratings_prepared = (
        ratings if "rating_datetime" in ratings.columns else prepare_ratings(ratings)
    )
    movies_prepared = (
        movies if "genre_list" in movies.columns else prepare_movies(movies)
    )
    tags_prepared = None
    if tags is not None:
        tags_prepared = tags if "tag_clean" in tags.columns else prepare_tags(tags)

    movie_rating_stats = (
        ratings_prepared.groupby("movieId", dropna=False)
        .agg(
            rating_count=("rating", "size"),
            avg_rating=("rating", "mean"),
            rating_std=("rating", "std"),
        )
        .reset_index()
        if not ratings_prepared.empty
        else _empty_movie_stats()
    )
    user_stats = (
        ratings_prepared.groupby("userId", dropna=False)
        .agg(
            rating_count=("rating", "size"),
            avg_rating=("rating", "mean"),
            rating_std=("rating", "std"),
        )
        .reset_index()
        if not ratings_prepared.empty
        else _empty_user_stats()
    )
    movie_stats = movies_prepared.merge(movie_rating_stats, on="movieId", how="left")
    movie_stats["rating_count"] = movie_stats["rating_count"].fillna(0).astype(int)

    exploded_genres = explode_genres(movies_prepared)
    rating_genre_df = ratings_prepared.merge(
        exploded_genres[["movieId", "title", "release_year", "genre"]],
        on="movieId",
        how="inner",
    )

    if tags_prepared is None:
        movie_tag_stats = pd.DataFrame(
            columns=[
                "movieId",
                "tag_application_count",
                "unique_tag_count",
                "unique_tag_users",
            ]
        )
    else:
        analysis_tags = tags_prepared.loc[~tags_prepared["tag_is_empty"]]
        movie_tag_stats = (
            analysis_tags.groupby("movieId", dropna=False)
            .agg(
                tag_application_count=("tag_clean", "size"),
                unique_tag_count=("tag_clean", "nunique"),
                unique_tag_users=("userId", "nunique"),
            )
            .reset_index()
        )

    return {
        "ratings": ratings_prepared,
        "movies": movies_prepared,
        "tags": tags_prepared if tags_prepared is not None else pd.DataFrame(),
        "movie_stats": movie_stats,
        "user_stats": user_stats,
        "exploded_genres": exploded_genres,
        "rating_genre_df": rating_genre_df,
        "movie_tag_stats": movie_tag_stats,
    }

