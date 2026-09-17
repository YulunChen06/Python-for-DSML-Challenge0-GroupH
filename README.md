# Python for DSML - Challenge 0 - Group H

This repo contains the leader-owned MovieLens-20M infrastructure and the
starter handoff notebooks for Persons B, C, and D.

## Run locally

From this directory:

    python -m pip install -r requirements.txt
    jupyter notebook notebooks/00_data_loading_and_eda.ipynb

The official dataset must be in data/ml-20m/. It is already downloaded in the
shared workspace. On another machine, download MovieLens-20M from
https://files.grouplens.org/datasets/movielens/ml-20m.zip, extract it, and
either use data/ml-20m/ or set MOVIELENS_DATA_DIR to its extracted folder.

Run notebooks in this order:

1. 00_data_loading_and_eda.ipynb: loading, quality checks, shared tables, and
   Level 1 EDA.
2. 01_user_temporal.ipynb: Person B assignment.
3. 02_genre_movie.ipynb: Person C assignment.
4. 03_tags_advanced.ipynb: Person D assignment.
5. final_submission.ipynb: leader integration after contributor handoffs.

## Shared definitions

- Movie popularity: number of rating records received.
- User activity: number of rating records given.
- Genre movie count: unique movies containing the genre.
- Genre rating means: rating-record means after exploding multi-genre movies.
- Challenge Question 1 support: movie rating_count >= 1000.
- User activity groups: bottom 50%, 50-90%, 90-99%, and top 1%.
- Movies with no listed genre are excluded from genre-attributed statistics.

## Files

- src/: shared loading, preprocessing, metrics, and plotting code.
- notebooks/00_data_loading_and_eda.ipynb: completed leader baseline.
- notebooks/01-03: starter notebooks for the three contributor assignments.
- TEAM_ASSIGNMENTS.md: coding tasks, handoff files, and review rules.
- notebooks/final_submission.ipynb: integration scaffold for Challenge Questions
  1-5.
- final_writeup.md: one-page write-up structure.
- outputs/summary_tables/: exported tables after a full run.
- figures/: exported plots after a full run.

The raw data directory is ignored because the CSV files exceed normal GitHub
file limits. The code and derived summary outputs are safe to commit.

