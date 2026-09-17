from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from load_data import load_movielens
from metrics import genre_pair_stats, genre_q1_table, genre_summary, tag_genome_comparison
from preprocess import build_shared_tables, prepare_genome_scores, prepare_genome_tags


def load_sample_tables():
    data_dir = PROJECT_ROOT / "data" / "sample"
    frames = load_movielens(data_dir)
    tables = build_shared_tables(frames["ratings"], frames["movies"], frames["tags"])
    return frames, tables


def test_shared_tables_and_definitions():
    _, tables = load_sample_tables()
    assert {"movie_stats", "user_stats", "exploded_genres", "rating_genre_df"} <= set(tables)
    assert tables["ratings"]["rating_datetime"].notna().all()
    assert tables["movies"]["release_year_parse_ok"].sum() == 10
    assert tables["movie_stats"]["rating_count"].max() == 5


def test_q1_and_q5_return_support_aware_tables():
    _, tables = load_sample_tables()
    genre_stats = genre_summary(tables["exploded_genres"], tables["rating_genre_df"])
    q1 = genre_q1_table(
        tables["movie_stats"],
        tables["rating_genre_df"],
        tables["exploded_genres"],
        min_movie_ratings=2,
    )
    pairs = genre_pair_stats(
        tables["ratings"], tables["movies"], genre_stats, min_movie_count=1
    )
    assert not genre_stats.empty
    assert set(q1["scope"]) == {"all movies", "movies with >= 2 ratings"}
    assert not pairs.empty
    assert "gain_vs_best_single" in pairs


def test_tag_genome_mapping_reports_matches():
    frames, tables = load_sample_tables()
    genome_scores = prepare_genome_scores(frames["genome-scores"])
    genome_tags = prepare_genome_tags(frames["genome-tags"])
    comparison = tag_genome_comparison(
        tables["tags"], genome_scores, genome_tags
    )
    assert not comparison.empty
    assert comparison["genome_tag_id"].notna().any()

