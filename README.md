# Python for DSML — Challenge 0 — Group H

This repository is the shared MovieLens-20M analysis project for Group H. The
leader-owned infrastructure keeps data loading, preprocessing, definitions,
quality checks, and baseline EDA consistent across all team notebooks.

## Project layout

```text
.
├── data/
│   ├── README.md
│   └── sample/                 # small smoke-test fixture, not the assignment data
├── figures/
├── notebooks/
│   ├── 00_data_loading_and_eda.ipynb
│   ├── 01_user_temporal.ipynb
│   ├── 02_genre_movie.ipynb
│   ├── 03_tags_advanced.ipynb
│   └── final_submission.ipynb
├── outputs/
│   ├── intermediate/
│   └── summary_tables/
├── src/
│   ├── load_data.py
│   ├── metrics.py
│   ├── plotting.py
│   └── preprocess.py
└── final_writeup.md
```

## Data setup

The full MovieLens-20M archive is not committed because it is large. Download
and extract it so the files below exist in `data/ml-20m/` (or set the
`MOVIELENS_DATA_DIR` environment variable to another directory):

```text
ratings.csv
movies.csv
tags.csv
links.csv
genome-scores.csv
genome-tags.csv
```

The notebooks automatically fall back to `data/sample/` when the full dataset
is not present. That fallback is only for smoke testing; all reported findings
for the course submission must use MovieLens-20M.

## Run

From this repository directory:

```powershell
python -m pip install -r requirements.txt
$env:MOVIELENS_DATA_DIR = "data/ml-20m"
jupyter notebook notebooks/00_data_loading_and_eda.ipynb
```

Run notebooks in this order:

1. `00_data_loading_and_eda.ipynb` — shared loading, quality checks, and Level 1 baseline.
2. `01_user_temporal.ipynb` — user activity and temporal handoff template.
3. `02_genre_movie.ipynb` — genre and multi-genre handoff template.
4. `03_tags_advanced.ipynb` — tags/genome handoff template.
5. `final_submission.ipynb` — integrated story and Challenge Questions 1–5.

## Shared definitions

- Movie popularity = number of rating records received by a movie.
- User activity = number of rating records given by a user.
- Genre movie count = unique movies containing that genre.
- Genre rating count and mean rating are calculated over rating records after
  exploding multi-genre movies. Therefore one rating can contribute to several
  genre rows; this is stated in every genre analysis.
- The `>=1000 ratings` filter in Challenge Question 1 means a movie-level
  rating count threshold, not a genre-level threshold.
- User activity groups use empirical percentiles: bottom 50%, 50–90%, 90–99%,
  and top 1%. No arbitrary fixed activity threshold is assumed.
- `(no genres listed)` is excluded from genre-attributed statistics but remains
  in movie-level counts.
- User tags are normalized only with lowercase and surrounding whitespace
  removal for the primary analysis. Hyphen-to-space normalization is used only
  for the explicitly labelled user-tag/genome-tag matching comparison.

## Runtime feasibility

MovieLens core files do not contain a runtime field. `links.csv` supplies IMDb
and TMDb identifiers, so a runtime trend is feasible only after joining a
reliable external metadata source. The project deliberately does not use title
length as a runtime proxy.

## Reproducibility

All notebooks import the same modules from `src/`, use project-relative paths,
export quality tables to `outputs/summary_tables/`, and save figures under
`figures/`. No notebook requires a personal absolute path.

