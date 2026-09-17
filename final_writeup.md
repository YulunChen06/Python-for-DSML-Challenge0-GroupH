# MovieLens-20M Challenge 0 — Group H

## Dataset and goal

We analyzed the MovieLens-20M ratings, movies, user tags, links, and tag-genome
files to describe rating behavior, genre structure, tag usage, and temporal
patterns. The project uses shared definitions for movie popularity, user
activity, genre support, and rating-level genre means so that the four analysis
threads remain comparable.

## Key findings

1. **Rating behavior.** After the full-data notebook run, report the rating
   distribution, mean, median, and the degree of skew toward higher ratings.
   Cite the exported rating summary rather than relying on a plot alone.

2. **User activity.** User activity is expected to be strongly right-skewed:
   compare the most active users with the bottom-50%, 50–90%, 90–99%, and top-1%
   empirical groups. The result is descriptive and does not establish that
   activity causes rating generosity or harshness.

3. **Genre and support.** Report the highest average-rating genre both before
   and after the movie-level 1000-rating support filter. Include movie count
   and rating count next to every mean; a high mean with little support is not
   evidence of popularity.

4. **Tags and genome.** Report the most frequent user tags, then compare
   normalized user-tag usage with genome relevance only for matched tags. State
   the exact matching coverage and discuss wording mismatch as a limitation.

5. **Multi-genre structure.** Report the highest-support genre pair only when it
   meets the minimum-support rule, and compare its average with the two
   individual genre averages. Because individual genre means include the pair
   movies, interpret the comparison as descriptive overlap rather than an
   independent effect.

## Interesting surprise

Complete this paragraph from the full-data outputs: identify one result that
changed after support filtering, one user-activity contrast, or one notable
user-tag/genome mismatch.

## Limitations and next step

The data are observational, multi-genre attribution duplicates rating records
across genres, older release years have uneven support, the final rating year
may be incomplete, and exact tag matching is conservative. Runtime is not
included in the MovieLens core files; a runtime trend requires an external
IMDb/TMDb metadata join and must not use title length as a proxy.

Before submission, replace the parameterized statements above with the
full-data values produced by final_submission.ipynb and attach the exported
summary tables and figures.

