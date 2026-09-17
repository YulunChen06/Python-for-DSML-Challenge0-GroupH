# MovieLens-20M Challenge 0 - Group H

## Dataset and goal

The leader pipeline was run on the official MovieLens-20M release:
20,000,263 ratings, 27,278 movies, 138,493 users, 465,564 tag applications,
and 11,709,768 genome-score rows. File-level quality checks found no duplicate
rows. The analysis describes rating behavior, genres, tags, and time trends.

## Key findings

1. Ratings are concentrated toward the upper half of the scale. The mean is
   3.526, the median is 3.5, and the mode is 4.0. The observed range is 0.5 to
   5.0.

2. User activity is strongly right-skewed. The median user gives 68 ratings,
   while the most active user gives 9,254. The top 1% activity group has a mean
   user average rating of 3.253, compared with 3.644 for the bottom 50%.
   This is descriptive and not causal.

3. Film-Noir has the highest rating-record mean: 3.965 across all movies and
   4.001 after retaining only movies with at least 1,000 ratings. The result
   should be read with movie and rating support, not as a popularity ranking.

4. The most frequently applied user tag is sci-fi with 3,576 applications,
   followed by based on a book with 3,307. Only 1,122 of 35,020 normalized
   non-empty user tags match a genome tag exactly after the documented
   normalization, a 3.20% vocabulary match rate.

5. With at least 50 movies per pair, Crime + Drama has the largest gain over
   the better individual genre mean: 3.794 versus 3.675, a gain of 0.120. The
   pair contains 1,677 movies and 1,682,632 rating records.

## Temporal and runtime notes

Rating activity varies by rating year. The 2015 data contain 283,886 ratings
and are not a complete calendar year, so the end-of-period decline must not be
interpreted as user loss. Runtime is not included in MovieLens-20M. links.csv
contains IMDb and TMDb identifiers, so a reliable runtime trend requires an
external metadata join; title length is not used as a proxy.

## Limitations and next step

The data are observational. Multi-genre movies contribute a rating record to
each constituent genre, older release years have uneven support, and exact
tag matching underestimates semantic agreement. The next step is for Persons
B, C, and D to complete their starter notebooks and hand back the required
tables and figures described in TEAM_ASSIGNMENTS.md.

