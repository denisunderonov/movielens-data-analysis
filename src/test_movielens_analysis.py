from collections import Counter

from movielens_analysis import Movies, Ratings


class TestMovies:
    def test_extract_year(self):
        movies = Movies()
        assert movies.extract_year("Toy Story (1995)") == 1995

    def test_get_movies(self):
        result = Movies().get_movies()

        assert isinstance(result, dict)
        assert len(result) > 0

        movie_id, movie_info = next(iter(result.items()))
        assert isinstance(movie_id, str)
        assert isinstance(movie_info, dict)
        assert isinstance(movie_info["title"], str)
        assert isinstance(movie_info["genres"], list)
        assert all(isinstance(genre, str) for genre in movie_info["genres"])

    def test_get_all_films_information(self):
        ratings = Ratings().get_ratings()
        movies = Movies().get_movies()
        result = Movies().get_all_films_information(ratings, movies)

        assert isinstance(result, list)
        assert len(result) > 0

        title, info = result[0]
        assert isinstance(title, str)
        assert isinstance(info["av_rating"], float)
        assert isinstance(info["reviews"], int)
        assert isinstance(info["genres"], list)
        assert info["year"] is None or isinstance(info["year"], int)

    def test_films_sorted(self):
        ratings = Ratings().get_ratings()
        movies = Movies().get_movies()
        result = Movies().get_all_films_information(ratings, movies)
        average_ratings = [film[1]["av_rating"] for film in result]

        assert average_ratings == sorted(average_ratings, reverse=True)

    def test_top_films(self):
        ratings = Ratings().get_ratings()
        movies = Movies().get_movies()
        films = Movies().get_all_films_information(ratings, movies)
        top_100 = Movies().get_top_100_films(films)

        assert len(top_100) == 100
        assert all(film[1]["reviews"] > 20 for film in top_100)

    def test_worst_films(self):
        ratings = Ratings().get_ratings()
        movies = Movies().get_movies()
        films = Movies().get_all_films_information(ratings, movies)
        worst_100 = Movies().get_worst_100_films(films)
        average_ratings = [film[1]["av_rating"] for film in worst_100]

        assert len(worst_100) == 100
        assert all(film[1]["reviews"] > 20 for film in worst_100)
        assert average_ratings == sorted(average_ratings)

    def test_top_and_worst_genres(self):
        films = [
            ("Film 1", {"genres": ["Drama", "Comedy"]}),
            ("Film 2", {"genres": ["Drama"]}),
        ]

        assert Movies().get_top_genres(films) == [("Drama", 2), ("Comedy", 1)]
        assert Movies().get_worst_genres(films) == [("Drama", 2), ("Comedy", 1)]

    def test_most_reviewed_films(self):
        films = [
            ("Film 1", {"reviews": 10}),
            ("Film 2", {"reviews": 30}),
            ("Film 3", {"reviews": 20}),
        ]
        result = Movies().get_most_rev_films(films)
        reviews = [film[1]["reviews"] for film in result]

        assert reviews == [30, 20, 10]
        assert len(result) <= 10

    def test_interesting_films(self):
        films = [
            ("Film 1", {"reviews": 5}),
            ("Film 2", {"reviews": 19}),
            ("Film 3", {"reviews": 20}),
            ("Film 4", {"reviews": 4}),
        ]
        result = Movies().get_interesting_films(films)

        assert len(result) == 2
        assert all(5 <= film[1]["reviews"] < 20 for film in result)

    def test_average_genre_rating(self):
        films = [
            ("Film 1", {"genres": ["Drama", "Comedy"], "av_rating": 4.0}),
            ("Film 2", {"genres": ["Drama"], "av_rating": 2.0}),
        ]
        result = Movies().get_av_genres_rating(films)

        assert result["Drama"] == 3.0
        assert result["Comedy"] == 4.0

    def test_year_analytics(self):
        films = [
            ("Film 1", {"year": 1991, "av_rating": 4.0, "reviews": 10}),
            ("Film 2", {"year": 1999, "av_rating": 2.0, "reviews": 20}),
            ("Film 3", {"year": None, "av_rating": 5.0, "reviews": 5}),
        ]
        result = Movies().get_year_analystics(films)

        assert result["90-е"]["av_rating"] == 3.0
        assert result["90-е"]["reviews"] == 30
        assert result["90-е"]["films"] == 2

    def test_empty_inputs(self):
        movies = Movies()

        assert movies.get_top_100_films([]) == []
        assert movies.get_worst_100_films([]) == []
        assert movies.get_top_genres([]) == []
        assert movies.get_year_analystics([]) == {}


class TestRatings:
    def test_get_ratings(self):
        result = Ratings().get_ratings()

        assert isinstance(result, list)
        assert len(result) > 0

        first_rating = result[0]
        assert isinstance(first_rating, dict)
        assert isinstance(first_rating["user_id"], str)
        assert isinstance(first_rating["movie_id"], str)
        assert isinstance(first_rating["rating"], str)

    def test_sort_user(self):
        ratings = [
            {"user_id": "1"},
            {"user_id": "1"},
            {"user_id": "2"},
        ]

        assert Ratings().sort_user(ratings) == [("1", 2), ("2", 1)]

    def test_count_ratings(self):
        ratings = [
            {"rating": "5.0"},
            {"rating": "4.0"},
            {"rating": "5.0"},
        ]

        assert Ratings().count_ratings(ratings) == Counter({"5.0": 2, "4.0": 1})

    def test_empty_inputs(self):
        ratings = Ratings()

        assert ratings.sort_user([]) == []
        assert ratings.count_ratings([]) == Counter()
