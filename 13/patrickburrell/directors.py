import csv
from collections import defaultdict, namedtuple
from pathlib import Path
import itertools

MOVIE_DATA = "movie_metadata.csv"
NUM_TOP_DIRECTORS = 20
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple("Movie", "title year score")


def get_movies_by_director():
    """Extracts all movies from csv and stores them in a dictionary
    where keys are directors, and values is a list of movies (named tuples)"""

    directors = {}
    folder = Path(__file__).parent
    with open(folder / MOVIE_DATA, newline="") as csvfile:
        reader = csv.reader(csvfile)
        columns = reader.__next__()

        director_index = columns.index("director_name")
        title_index = columns.index("movie_title")
        year_index = columns.index("title_year")
        score_index = columns.index("imdb_score")

        for row in reader:
            director = row[director_index]
            movie = Movie(
                title=row[title_index],
                year=_try_int(row[year_index]),
                score=float(row[score_index]),
            )

            if director not in directors:
                directors[director] = {"movies": []}
            if movie.year >= MIN_YEAR:
                directors[director]["movies"].append(movie)

    return directors


def get_average_scores(directors):
    """Filter directors with < MIN_MOVIES and calculate averge score"""

    directors = {k: v for k, v in directors.items() if len(v["movies"]) >= MIN_MOVIES}

    for director in directors:
        directors[director]["mean_score"] = _calc_mean(directors[director]["movies"])

    return directors


def _calc_mean(movies):
    """Helper method to calculate mean of list of Movie namedtuples"""
    sum = 0.0
    for movie in movies:
        sum += movie.score
    mean = sum / len(movies)
    return mean


def _try_int(s):
    try:
        i = int(s)
    except ValueError:
        i = 0  # the default value
    return i


def print_results(directors):
    """Print directors ordered by highest average rating. For each director
    print his/her movies also ordered by highest rated movie.
    See http://pybit.es/codechallenge13.html for example output"""
    fmt_director_entry = "{counter:02d}. {director:<52} {avg:.1f}"
    fmt_movie_entry = "{year}] {title:<50} {score}"
    sep_line = "-" * 60

    ordered_directors = {
        k: v
        for k, v in sorted(
            directors.items(), key=lambda item: item[1]["mean_score"], reverse=True
        )
    }

    top20_directors = dict(
        itertools.islice(ordered_directors.items(), NUM_TOP_DIRECTORS)
    )

    for i, (k, v) in enumerate(top20_directors.items()):
        print(fmt_director_entry.format(counter=i + 1, director=k, avg=v["mean_score"]))
        print(sep_line)

        movies = v["movies"]
        ordered_movies = [
            m for m in sorted(movies, key=lambda item: item.score, reverse=True)
        ]

        for movie in ordered_movies:
            print(
                fmt_movie_entry.format(
                    year=movie.year, title=movie.title, score=movie.score
                )
            )
        print("\n")


def main():
    """This is a template, feel free to structure your code differently.
    We wrote some tests based on our solution: test_directors.py"""

    directors = get_movies_by_director()
    directors = get_average_scores(directors)
    print_results(directors)


if __name__ == "__main__":
    main()
