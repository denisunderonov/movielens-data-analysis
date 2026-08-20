import pytest
from movielens_analysis import Links, Tags

# Убедись, что имена файлов совпадают с твоими
LINKS_FILE = 'links.csv'
TAGS_FILE = 'tags.csv'


# ═══════════════════════════════════════════════════════════════
# ТЕСТЫ ДЛЯ КЛАССА LINKS (11 методов = 11 тестов)
# ═══════════════════════════════════════════════════════════════
class TestLinks:

    @pytest.fixture
    def links(self):
        # Создание объекта (тестирует __init__)
        return Links(LINKS_FILE)

    # 1. Тест для get_all
    def test_get_all(self, links):
        result = links.get_all()
        assert isinstance(result, list)                  # Проверка типа возврата
        assert all(isinstance(x, dict) for x in result)  # Проверка типов элементов списка

    # 2. Тест для get_link
    def test_get_link(self, links):
        result = links.get_link(1)
        assert isinstance(result, dict)                  # Проверка типа возврата

    # 3. Тест для get_only_imdbId
    def test_get_only_imdbId(self, links):
        result = links.get_only_imdbId(1)
        assert isinstance(result, str)                   # Проверка типа возврата

    # 4. Тест для get_only_movieId
    def test_get_only_movieId(self, links):
        result = links.get_only_movieId(1)
        assert isinstance(result, int)                   # Проверка типа возврата

    # 5. Тест для get_only_tmdbId
    def test_get_only_tmdbId(self, links):
        result = links.get_only_tmdbId(1)
        # tmdbId может быть int или None (если в файле пусто)
        assert isinstance(result, int) or result is None 

    # 6. Тест для get_movielens_link
    def test_get_movielens_link(self, links):
        result = links.get_movielens_link(1)
        assert isinstance(result, str)                   # Проверка типа возврата

    # 7. Тест для get_imdb_link
    def test_get_imdb_link(self, links):
        result = links.get_imdb_link(1)
        assert isinstance(result, str)                   # Проверка типа возврата

    # 8. Тест для get_themoviedb_link
    def test_get_themoviedb_link(self, links):
        result = links.get_themoviedb_link(1)
        assert isinstance(result, str) or result is None # Проверка типа возврата

    # 9. Тест для get_count
    def test_get_count(self, links):
        result = links.get_count()
        assert isinstance(result, int)                   # Проверка типа возврата
        assert result == 1000                            # Проверка значения (по заданию)

    # 10. Тест для get_all_movie_ids
    def test_get_all_movie_ids(self, links):
        result = links.get_all_movie_ids()
        assert isinstance(result, list)                  # Проверка типа возврата
        assert all(isinstance(x, int) for x in result)   # Проверка типов элементов списка
        assert result == sorted(result)                  # Проверка сортировки

    # 11. Тест для has_movie
    def test_has_movie(self, links):
        result = links.has_movie(1)
        assert isinstance(result, bool)                  # Проверка типа возврата


# ═══════════════════════════════════════════════════════════════
# ТЕСТЫ ДЛЯ КЛАССА TAGS (11 методов = 11 тестов)
# ═══════════════════════════════════════════════════════════════
class TestTags:

    @pytest.fixture
    def tags(self):
        # Создание объекта (тестирует __init__)
        return Tags(TAGS_FILE)

    # 1. Тест для get_all
    def test_get_all(self, tags):
        result = tags.get_all()
        assert isinstance(result, list)                  # Проверка типа возврата
        assert all(isinstance(x, dict) for x in result)  # Проверка типов элементов списка

    # 2. Тест для get_tags_by_movie_with_dates
    def test_get_tags_by_movie_with_dates(self, tags):
        # Берем фильм 1. Если в твоих данных его нет, можешь заменить на любой другой ID
        result = tags.get_tags_by_movie_with_dates(1)    
        assert isinstance(result, list)                  # Проверка типа возврата
        assert all(isinstance(x, dict) for x in result)  # Проверка типов элементов списка
        timestamps = [x['timestamp'] for x in result]
        assert timestamps == sorted(timestamps)          # Проверка сортировки

    # 3. Тест для get_tags_film
    def test_get_tags_film(self, tags):
        result = tags.get_tags_film(1)
        assert isinstance(result, list)                  # Проверка типа возврата
        assert all(isinstance(x, str) for x in result)   # Проверка типов элементов списка

    # 4. Тест для get_tags_user
    def test_get_tags_user(self, tags):
        result = tags.get_tags_user(2)
        assert isinstance(result, list)                  # Проверка типа возврата
        assert all(isinstance(x, str) for x in result)   # Проверка типов элементов списка

    # 5. Тест для get_most_popular_tags
    def test_get_most_popular_tags(self, tags):
        result = tags.get_most_popular_tags(5)
        assert isinstance(result, list)                  # Проверка типа возврата
        assert all(isinstance(x, tuple) for x in result) # Проверка типов элементов списка
        counts = [x[1] for x in result]
        assert counts == sorted(counts, reverse=True)    # Проверка сортировки (по убыванию)

    # 6. Тест для get_unique_tags
    def test_get_unique_tags(self, tags):
        result = tags.get_unique_tags()
        assert isinstance(result, list)                  # Проверка типа возврата
        assert all(isinstance(x, str) for x in result)   # Проверка типов элементов списка
        assert result == sorted(result)                  # Проверка сортировки (по алфавиту)

    # 7. Тест для get_unique_tags_count
    def test_get_unique_tags_count(self, tags):
        result = tags.get_unique_tags_count()
        assert isinstance(result, int)                   # Проверка типа возврата

    # 8. Тест для get_movies_by_tag
    def test_get_movies_by_tag(self, tags):
        result = tags.get_movies_by_tag('funny')
        assert isinstance(result, list)                  # Проверка типа возврата
        assert all(isinstance(x, int) for x in result)   # Проверка типов элементов списка
        assert result == sorted(result)                  # Проверка сортировки

    # 9. Тест для get_user_activity
    def test_get_user_activity(self, tags):
        result = tags.get_user_activity()
        assert isinstance(result, list)                  # Проверка типа возврата
        assert all(isinstance(x, tuple) for x in result) # Проверка типов элементов списка
        counts = [x[1] for x in result]
        assert counts == sorted(counts, reverse=True)    # Проверка сортировки (по убыванию)

    # 10. Тест для get_tags_count
    def test_get_tags_count(self, tags):
        result = tags.get_tags_count()
        assert isinstance(result, int)                   # Проверка типа возврата
        assert result == 1000                            # Проверка значения (по заданию)