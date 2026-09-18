# Dataset provenance

The assignment PDF specifies the Kaggle [MovieLens 20M Dataset](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset).
The local working copy in `data/ml-20m/` is the matching MovieLens-20M
release and contains:

    ratings.csv
    movies.csv
    tags.csv
    links.csv
    genome-scores.csv
    genome-tags.csv

The Kaggle page is the source to cite and use when recreating the environment.
The current notebooks expect the files to already be present; they do not
download data automatically. The full data directory is ignored by Git because
the CSV files are too large for a normal GitHub commit. Do not replace it with
MovieLens latest or another MovieLens version: the assignment requires
MovieLens-20M.
