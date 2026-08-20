import pytest
from movielens_analysis import Links, Tags

# Убедись, что имена файлов совпадают с твоими
LINKS_FILE = 'links.csv'
TAGS_FILE = 'tags.csv'


class TestLinks:
    """Класс, содержащий набор тестов для проверки методов класса Links."""

    @pytest.fixture
    def links(self):
        """Фикстура для создания объекта Links перед каждым тестом."""
        return Links(LINKS_FILE)

    def test_get_all(self, links):
        """Тестирует метод get_all: проверяет возврат списка, состоящего из словарей."""
        result = links.get_all()
        assert isinstance(result, list)
        assert all(isinstance(x, dict) for x in result)

    def test_get_link(self, links):
        """Тестирует метод get_link: проверяет возврат словаря для существующего ID."""
        result = links.get_link(1)
        assert isinstance(result, dict)

    def test_get_only_imdbId(self, links):
        """Тестирует метод get_only_imdbId: проверяет возврат строки."""
        result = links.get_only_imdbId(1)
        assert isinstance(result, str)

    def test_get_only_movieId(self, links):
        """Тестирует метод get_only_movieId: проверяет возврат целого числа."""
        result = links.get_only_movieId(1)
        assert isinstance(result, int)

    def test_get_only_tmdbId(self, links):
        """Тестирует метод get_only_tmdbId: проверяет возврат целого числа или None."""
        result = links.get_only_tmdbId(1)
        assert isinstance(result, int) or result is None

    def test_get_movielens_link(self, links):
        """Тестирует метод get_movielens_link: проверяет возврат строки-ссылки."""
        result = links.get_movielens_link(1)
        assert isinstance(result, str)

    def test_get_imdb_link(self, links):
        """Тестирует метод get_imdb_link: проверяет возврат строки-ссылки."""
        result = links.get_imdb_link(1)
        assert isinstance(result, str)

    def test_get_themoviedb_link(self, links):
        """Тестирует метод get_themoviedb_link: проверяет возврат строки-ссылки или None."""
        result = links.get_themoviedb_link(1)
        assert isinstance(result, str) or result is None

    def test_get_count(self, links):
        """Тестирует метод get_count: проверяет возврат целого числа и значение 1000."""
        result = links.get_count()
        assert isinstance(result, int)
        assert result == 1000

    def test_get_all_movie_ids(self, links):
        """Тестирует метод get_all_movie_ids: проверяет тип списка, тип элементов и сортировку."""
        result = links.get_all_movie_ids()
        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)
        assert result == sorted(result)

    def test_has_movie(self, links):
        """Тестирует метод has_movie: проверяет возврат булевого значения (True/False)."""
        result = links.has_movie(1)
        assert isinstance(result, bool)


class TestTags:
    """Класс, содержащий набор тестов для проверки методов класса Tags."""

    @pytest.fixture
    def tags(self):
        """Фикстура для создания объекта Tags перед каждым тестом."""
        return Tags(TAGS_FILE)

    def test_get_all(self, tags):
        """Тестирует метод get_all: проверяет возврат списка, состоящего из словарей."""
        result = tags.get_all()
        assert isinstance(result, list)
        assert all(isinstance(x, dict) for x in result)

    def test_get_tags_by_movie_with_dates(self, tags):
        """Тестирует метод get_tags_by_movie_with_dates: проверяет типы данных и сортировку по времени."""
        result = tags.get_tags_by_movie_with_dates(1)
        assert isinstance(result, list)
        assert all(isinstance(x, dict) for x in result)
        timestamps = [x['timestamp'] for x in result]
        assert timestamps == sorted(timestamps)

    def test_get_tags_film(self, tags):
        """Тестирует метод get_tags_film: проверяет возврат списка строк."""
        result = tags.get_tags_film(1)
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)

    def test_get_tags_user(self, tags):
        """Тестирует метод get_tags_user: проверяет возврат списка строк."""
        result = tags.get_tags_user(2)
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)

    def test_get_most_popular_tags(self, tags):
        """Тестирует метод get_most_popular_tags: проверяет список кортежей и сортировку по убыванию."""
        result = tags.get_most_popular_tags(5)
        assert isinstance(result, list)
        assert all(isinstance(x, tuple) for x in result)
        counts = [x[1] for x in result]
        assert counts == sorted(counts, reverse=True)

    def test_get_unique_tags(self, tags):
        """Тестирует метод get_unique_tags: проверяет список строк и алфавитную сортировку."""
        result = tags.get_unique_tags()
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)
        assert result == sorted(result)

    def test_get_unique_tags_count(self, tags):
        """Тестирует метод get_unique_tags_count: проверяет возврат целого числа."""
        result = tags.get_unique_tags_count()
        assert isinstance(result, int)

    def test_get_movies_by_tag(self, tags):
        """Тестирует метод get_movies_by_tag: проверяет список целых чисел и сортировку по возрастанию."""
        result = tags.get_movies_by_tag('funny')
        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)
        assert result == sorted(result)

    def test_get_user_activity(self, tags):
        """Тестирует метод get_user_activity: проверяет список кортежей и сортировку по убыванию."""
        result = tags.get_user_activity()
        assert isinstance(result, list)
        assert all(isinstance(x, tuple) for x in result)
        counts = [x[1] for x in result]
        assert counts == sorted(counts, reverse=True)

    def test_get_tags_count(self, tags):
        """Тестирует метод get_tags_count: проверяет возврат целого числа и значение 1000."""
        result = tags.get_tags_count()
        assert isinstance(result, int)
        assert result == 1000