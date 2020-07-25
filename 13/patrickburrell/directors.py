import csv
from collections import defaultdict, namedtuple, Counter
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

    movies_by_director = defaultdict(list)
    folder = Path(__file__).parent
    with open(folder / MOVIE_DATA) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                director = row["director_name"]
                movie = Movie(
                    title=row["movie_title"],
                    year=int(row["title_year"]),
                    score=float(row["imdb_score"]),
                )
            except ValueError:
                continue
            movies_by_director[director].append(movie)

    return movies_by_director


def get_average_scores(directors):
    """Filter directors with < MIN_MOVIES and calculate averge score"""

    directors = {k: v for k, v in directors.items() if len(v) >= MIN_MOVIES}

    score_ranks = defaultdict(list)
    for director, movies in directors.items():
        score_ranks[director].append(_calc_mean(movies))

    score_ranks = Counter(score_ranks).most_common(NUM_TOP_DIRECTORS)

    return directors, score_ranks


def _calc_mean(movies):
    """Helper method to calculate mean of list of Movie namedtuples"""
    mean = round(sum(movie.score for movie in movies) / len(movies), 1)
    return mean


def print_results(directors, score_ranks):
    """Print directors ordered by highest average rating. For each director
    print his/her movies also ordered by highest rated movie.
    See http://pybit.es/codechallenge13.html for example output"""
    fmt_director_entry = "{counter:02d}. {director:<52} {avg:.1f}"
    fmt_movie_entry = "{year}] {title:<50} {score}"
    sep_line = "-" * 60

    for i in range(len(score_ranks)):
        director = score_ranks[i][0]
        average = score_ranks[i][1][0]
        print(fmt_director_entry.format(counter=i + 1, director=director, avg=average))
        print(sep_line)

        movies = directors[director]
        sorted_movies = [
            m for m in sorted(movies, key=lambda item: item.score, reverse=True)
        ]

        for movie in sorted_movies:
            print(
                fmt_movie_entry.format(
                    year=movie.year, title=movie.title, score=movie.score
                )
            )

        print()


def main():
    """This is a template, feel free to structure your code differently.
    We wrote some tests based on our solution: test_directors.py"""

    directors = get_movies_by_director()
    directors, score_ranks = get_average_scores(directors)
    print_results(directors, score_ranks)


if __name__ == "__main__":
    main()
