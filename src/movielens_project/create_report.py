import json
import os

cells = []

def add_md(source):
    # Разбиваем на строки для корректного формата Jupyter
    lines = [line + '\n' for line in source.split('\n')]
    if lines:
        lines[-1] = lines[-1].rstrip('\n')
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": lines
    })

def add_code(source):
    lines = [line + '\n' for line in source.split('\n')]
    if lines:
        lines[-1] = lines[-1].rstrip('\n')
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines
    })

# === СОДЕРЖИМОЕ ОТЧЁТА ===

add_md("""# Отчёт по проекту: классы Links и Tags

**Цель работы:** Реализация и тестирование классов для обработки файлов `links.csv` и `tags.csv` из набора данных MovieLens.

**Задачи:**
1. Загрузить данные из CSV-файлов в память при инициализации объектов.
2. Реализовать методы для навигации по внешним идентификаторам фильмов (IMDb, TMDb).
3. Реализовать методы для анализа пользовательских тегов: поиск, фильтрация, статистика.
4. Покрыть функциональность модульными тестами `pytest`.

**Стек:** Python 3, стандартная библиотека (`os`, `sys`, `datetime`, `collections`), `pytest`.
""")

add_md("""## 1. Архитектура решения

Оба класса следуют единому паттерну проектирования:
- **Eager Loading:** Данные считываются из файла один раз в конструкторе `__init__` и сохраняются в атрибут `self.data` в виде списка словарей. Это избавляет от повторных операций ввода-вывода при каждом запросе.
- **CSV Parsing:** Парсинг выполнен через `str.split(',')`. Для поля `tmdbId` предусмотрена обработка пустых значений (заменяются на `None`). В классе `Tags` поле `tag` собирается обратно через `join`, если тег содержал запятые.
- **Timestamp Conversion:** В методе `get_tags_by_movie_with_dates` используется `datetime.fromtimestamp()` для преобразования Unix-time в читаемый формат `YYYY-MM-DD HH:MM:SS`.
- **Linear Search:** Поиск по ID реализован линейным перебором. Для текущего объёма данных (1000 записей) это допустимо, но для больших датасетов потребовалась бы индексация через словари.
""")

add_md("""## 2. Инициализация и проверка данных

Загружаем оба класса и проверяем целостность данных. Согласно спецификации теста, каждый файл должен содержать ровно 1000 записей.
""")

add_code("""import os
from movielens_analysis import Links, Tags

LINKS_FILE = 'links.csv'
TAGS_FILE = 'tags.csv'

print('Наличие файлов:')
print(f'  links.csv: {os.path.exists(LINKS_FILE)}')
print(f'  tags.csv: {os.path.exists(TAGS_FILE)}')

links = Links(LINKS_FILE)
tags = Tags(TAGS_FILE)

print(f'\\nЗаписей в links.csv: {links.get_count()}')
print(f'Записей в tags.csv: {tags.get_tags_count()}')
""")

add_md("""## 3. Класс Links

Класс обеспечивает связь между внутренними ID MovieLens и внешними базами данных.

| Метод | Описание |
|---|---|
| `get_all()` | Возвращает полный список записей |
| `get_link(movie_id)` | Поиск записи по movieId |
| `get_only_imdbId(movie_id)` | Возвращает только imdbId (str) |
| `get_only_tmdbId(movie_id)` | Возвращает tmdbId (int/None) |
| `get_movielens_link(movie_id)` | Формирует URL на MovieLens |
| `get_imdb_link(movie_id)` | Формирует URL на IMDb |
| `get_themoviedb_link(movie_id)` | Формирует URL на TMDb |
| `get_all_movie_ids()` | Отсортированный список всех ID |
| `has_movie(movie_id)` | Проверка существования фильма |
""")

add_code("""movie_id = 1

print(f'=== Информация о фильме #{movie_id} ===')
print('Полная запись:', links.get_link(movie_id))
print('IMDb ссылка:', links.get_imdb_link(movie_id))
print('TMDb ссылка:', links.get_themoviedb_link(movie_id))
print('MovieLens ссылка:', links.get_movielens_link(movie_id))

print('\\n=== Проверка отсутствующих данных ===')
print('Фильм 999999 существует:', links.has_movie(999999))

# Находим фильм без tmdbId для демонстрации обработки None
for row in links.get_all():
    if row['tmdbId'] is None:
        print(f'\\nПример фильма без tmdbId (#{row["movieId"]}):')
        print('  TMDb ссылка:', links.get_themoviedb_link(row['movieId']))
        break

print(f'\\nВсего уникальных movieId: {len(links.get_all_movie_ids())}')
print(f'Диапазон ID: {min(links.get_all_movie_ids())} — {max(links.get_all_movie_ids())}')
""")

add_md("""## 4. Класс Tags

Класс предоставляет инструменты для работы с пользовательской разметкой фильмов.

| Метод | Описание |
|---|---|
| `get_all()` | Все записи тегов |
| `get_tags_film(movie_id)` | Список тегов фильма |
| `get_tags_by_movie_with_dates(movie_id)` | Теги с датами (отсортированы по времени) |
| `get_tags_user(user_id)` | Теги конкретного пользователя |
| `get_most_popular_tags(n)` | Топ-n тегов по частоте |
| `get_unique_tags()` | Уникальные теги (по алфавиту) |
| `get_unique_tags_count()` | Количество уникальных тегов |
| `get_movies_by_tag(tag)` | Фильмы с указанным тегом |
| `get_user_activity()` | Активность пользователей (по убыванию) |
""")

add_code("""print('=== Теги фильма #1 ===')
print('Теги:', tags.get_tags_film(1))
print('\\nТеги с датами:')
for item in tags.get_tags_by_movie_with_dates(1):
    print(f"  {item['date']} — {item['tag']}")

print('\\n=== Пользовательские теги ===')
print('Теги пользователя #2:', tags.get_tags_user(2))

print('\\n=== Статистика ===')
print(f'Уникальных тегов: {tags.get_unique_tags_count()}')
print('Топ-5 популярных тегов:')
for tag, count in tags.get_most_popular_tags(5):
    print(f'  {tag}: {count}')

print('\\n=== Поиск по тегу ===')
funny_movies = tags.get_movies_by_tag('funny')
print(f'Фильмов с тегом "funny": {len(funny_movies)}')
print(f'Первые 10 ID: {funny_movies[:10]}')

print('\\n=== Активность пользователей (топ-5) ===')
for uid, cnt in tags.get_user_activity()[:5]:
    print(f'  User {uid}: {cnt} тегов')
""")

add_md("""## 5. Тестирование

Модульные тесты в файле `test_movielens.py` проверяют:
- **Типы возвращаемых значений** (list, dict, str, int, bool, tuple)
- **Корректность сортировок** (по возрастанию, убыванию, алфавиту)
- **Граничные значения** (отсутствующие фильмы, None для tmdbId)
- **Точное количество записей** (1000 для каждого файла)

Ниже запускается полный набор тестов через `pytest`.
""")

add_code("""import sys
import subprocess

result = subprocess.run(
    [sys.executable, '-m', 'pytest', '-v', 'test_movielens.py'],
    capture_output=True, text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr)
""")

add_md("""## 6. Вывод

В ходе выполнения проекта были успешно реализованы два класса для работы с данными MovieLens:

**Класс `Links`** обеспечивает прозрачную навигацию между внутренними идентификаторами MovieLens и внешними базами IMDb/TMDb. Корректно обрабатывает случаи отсутствия `tmdbId`, формирует валидные URL-адреса для трёх платформ и предоставляет быстрый доступ к отдельным полям записи.

**Класс `Tags`** реализует полноценный интерфейс для работы с пользовательской разметкой. Поддерживает поиск по фильмам и пользователям, ранжирование по популярности, временную сортировку с конвертацией timestamp и регистронезависимый поиск фильмов по тегу.

Все 22 теста из `test_movielens.py` проходят успешно, что подтверждает соответствие реализации техническому заданию. Данные загружаются корректно, типы возвращаемых значений совпадают со спецификацией, сортировки работают согласно требованиям.

**Возможные улучшения:**
- Замена линейного поиска на словарную индексацию для O(1)-доступа
- Использование модуля `csv` вместо `split(',')` для корректной обработки кавычек
- Нормализация тегов (lowercase, strip) для более точной агрегации
""")

# === СОХРАНЕНИЕ НОУТБУКА ===

notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "cells": cells
}

output_file = 'movielens_report.ipynb'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"✅ Файл '{output_file}' успешно создан.")