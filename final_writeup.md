# MovieLens-20M Challenge 0 - Group H

## Current leader deliverable

The leader has prepared the official MovieLens-20M loading pipeline, shared
preprocessing tables, file/key quality checks, dataset scale, the global rating
baseline, and the runtime feasibility investigation. The contributor findings
are intentionally not written here yet; Persons B, C, and D must complete and
hand off their own analyses first.

## Leader-owned checks

- Dataset files, row counts, missing cells, duplicate rows, and join coverage
  are exported under `outputs/summary_tables/`.
- Shared tables are defined in `src/preprocess.py`: `ratings`, `movies`,
  `movie_stats`, `user_stats`, `exploded_genres`, `rating_genre_df`, and
  `movie_tag_stats`.
- The global rating distribution is exported as
  `rating_counts.csv`, `rating_summary.csv`, and
  `figures/rating_distribution.png`.
- Runtime is not present in the supplied MovieLens files. A reliable runtime
  trend requires a reproducible external metadata join through IMDb/TMDb IDs;
  title length is not used as a proxy.

## Contributor handoffs still required

### Person B

Complete user activity, Challenge Question 2, rating-year and release-year
trends, the two-decade comparison, figures, findings, and limitations.

### Person C

Complete genre statistics, Challenge Questions 1 and 5, single/multi-genre
analysis, genre-count analysis, pair support, decade prominence, figures,
findings, and limitations.

### Person D

Complete tag cleaning and coverage, tag/popularity analysis, genome coverage,
selected movie profiles, Challenge Question 3, the stretch goal decision,
figures, findings, and limitations.

## Final integration rule

Only after the three handoffs pass the leader review should their evidence be
inserted into `notebooks/final_submission.ipynb` and this write-up. No
contributor result is pre-filled by the leader.
