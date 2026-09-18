# Group H - contributor coding assignments

The leader has prepared the shared data contract and the PDF Level 1 baseline
infrastructure. The Level 1 genre/user summaries in notebook 00 are context
only; they do not answer the contributor Challenge Questions.
Each contributor owns the implementation and interpretation of one notebook.
The repository intentionally does not contain completed contributor results;
the handoff files below are assignments, not files for the leader to fill in.
Do not duplicate or redefine the shared loading logic in src/.

## Shared contract for everyone

Start from the prepared tables created by build_shared_tables:

- ratings: rating timestamp plus rating_year, rating_month, and rating_dayofweek.
- movies: parsed release_year, release_year_parse_ok, genre_list, genre_count,
  is_multigenre, and release_decade.
- movie_stats: movie popularity and rating summary.
- user_stats: user activity and rating summary.
- exploded_genres: one row per movie-genre pair.
- rating_genre_df: rating records joined to genres; multi-genre ratings appear
  once per genre.
- movie_tag_stats: tag application and tag coverage by movie.

Use project-relative paths. Every analysis section must have:

1. Question
2. Data and columns
3. Method
4. Result table
5. Labeled visualization
6. Interpretation
7. Limitation

Do not change the definitions of popularity, activity, genre support, or the
1000-rating movie filter without a written note and leader review.

## Person B - user behavior and temporal trends

Notebook: notebooks/01_user_temporal.ipynb

Write code that:

- summarizes user_stats.rating_count with min, quartiles, mean, 90th, 95th,
  99th percentile, and max;
- identifies the top 20 active users and compares them with the percentile
  activity groups;
- plots ratings per user on linear and log-scaled axes;
- aggregates rating count and average rating by rating_year;
- aggregates rating behavior by release_year, with an explicit minimum
  rating-record support rule;
- compares two decades using movie count, rating count, average/median rating,
  variance, and user rating behavior;
- measures rating variance versus genre diversity for a clearly defined active-
  user subset, as requested by the PDF's advanced questions.

Required handoff:

- Challenge Question 2 answer;
- outputs/user_activity_summary.csv;
- outputs/ratings_by_year.csv;
- outputs/release_year_stats.csv;
- outputs/decade_comparison.csv;
- outputs/genre_diversity_variance.csv;
- labeled figures for activity and temporal trends;
- a labeled genre-diversity/variance figure;
- three findings, two limitations, and every threshold used.

Review traps: never confuse rating year with release year, never interpret an
incomplete final rating year as a full-year drop, and do not make causal claims.

## Person C - genre and movie analysis

Notebook: notebooks/02_genre_movie.ipynb

Write code that:

- reports genre movie count, rating count, mean, median, standard deviation,
  and variance;
- answers Challenge Question 1 before and after the movie-level
  rating_count >= 1000 filter;
- compares single-genre and multi-genre movies;
- analyzes genre_count against rating and popularity with support shown;
- builds genre pairs using combinations, applies a minimum-support rule, and
  compares each pair with both individual genres;
- compares genre prominence across the same two decades selected by Person B.

Required handoff:

- Challenge Questions 1 and 5 answers;
- outputs/genre_stats.csv;
- outputs/q1_genre_comparison.csv;
- outputs/multigenre_comparison.csv;
- outputs/genre_pair_stats.csv;
- outputs/decade_genre_prominence.csv;
- top-genre, rating-distribution, pair-gain, and decade-prominence figures;
- three findings, two limitations, and every support threshold used.

Review traps: a high average is not popularity, multi-genre attribution is
duplicated by design, and a pair with very few movies must not become a finding.

## Person D - tags and tag genome

Notebook: notebooks/03_tags_advanced.ipynb

Write code that:

- cleans user tags with lowercase and surrounding whitespace removal;
- reports tag application frequency separately from movie and user coverage;
- summarizes tags per movie and relates tag counts to movie popularity using
  support-aware count metrics and Spearman correlation;
- checks genome coverage and relevance ranges;
- selects representative movies with genome coverage and lists their top
  genome tags;
- compares genome relevance profiles across selected genres and reports
  support for the comparison;
- compares user tags with genome tags using exact normalized matching first,
  then labels any qualitative semantic comparison separately;
- reports matched-tag coverage and identifies high-frequency/low-relevance and
  low-frequency/high-relevance cases;
- completes one documented stretch goal, preferably a leakage-safe rating
  baseline with a train/test split.

Required handoff:

- Challenge Question 3 answer;
- outputs/tag_frequency.csv;
- outputs/movie_tag_stats.csv;
- outputs/user_tag_genome_comparison.csv;
- outputs/selected_movie_genome_tags.csv;
- outputs/genre_genome_profiles.csv;
- outputs/baseline_predictor_rmse.csv if the stretch goal is attempted;
- tag, genome, genre-profile, and tag-versus-popularity figures;
- three findings, two limitations, normalization rules, match coverage, and
  stretch-goal methodology.

Review traps: user tags and genome tags are not synonyms, exact matching is
conservative, and computing user/movie means before a train/test split leaks
test information.

## Leader review before integration

The leader will check that every handoff:

- uses the shared tables and definitions;
- exports the required tables and figures;
- states sample sizes and minimum-support rules;
- distinguishes descriptive evidence from causal claims;
- uses no personal absolute paths;
- runs top-to-bottom on a clean environment with MovieLens-20M;
- has a concise Challenge Question answer that can be copied into the final
  notebook and final_writeup.md.
