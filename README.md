# Python for DSML - Challenge 0 - Group H

This repo contains the leader-owned MovieLens-20M infrastructure and empty
assignment scaffolds for Persons B, C, and D. Contributor analyses are not
pre-computed here.

## Run locally

From this directory:

    python -m pip install -r requirements.txt
    jupyter notebook notebooks/00_data_loading_and_eda.ipynb

The official dataset must be in `data/ml-20m/`. It is already downloaded in
the shared workspace. On another machine, download MovieLens-20M from
https://files.grouplens.org/datasets/movielens/ml-20m.zip, extract it, and use
`data/ml-20m/` or set `MOVIELENS_DATA_DIR` to the extracted folder.

Run notebooks in this order:

1. `00_data_loading_and_eda.ipynb`: leader loading, quality checks, shared
   tables, dataset scale, rating baseline, and runtime feasibility.
2. `01_user_temporal.ipynb`: Person B assignment.
3. `02_genre_movie.ipynb`: Person C assignment.
4. `03_tags_advanced.ipynb`: Person D assignment.
5. `final_submission.ipynb`: integration only after all handoffs are complete.

## Shared definitions

- Movie popularity: number of rating records received.
- User activity: number of rating records given.
- Genre movie count: unique movies containing the genre.
- Genre rating means: rating-record means after exploding multi-genre movies.
- Challenge Question 1 support: movie `rating_count >= 1000`.
- Movies with no listed genre are excluded from genre-attributed statistics.

## Files

- `src/load_data.py`: loading and file summaries.
- `src/preprocess.py`: shared cleaning and derived tables only.
- `src/metrics.py`: leader-owned quality, rating, and runtime checks only.
- `src/plotting.py`: leader-owned global rating plot only.
- `notebooks/00_data_loading_and_eda.ipynb`: leader infrastructure notebook.
- `notebooks/01-03`: coding assignments, with TODOs and no completed findings.
- `TEAM_ASSIGNMENTS.md`: task definitions, handoff files, and review rules.
- `notebooks/final_submission.ipynb`: handoff readiness and integration template.
- `final_writeup.md`: leader status and post-handoff write-up template.

The raw data directory is ignored because the CSV files exceed normal GitHub
file limits. The code and leader-owned baseline outputs are safe to commit.
