# MovieLens Data Analysis
# Анализ данных MovieLens

A Python project that explores the MovieLens dataset through ratings, movies, genres, tags, external links, and user activity. The results are presented as an interactive Jupyter Notebook report.
Проект на Python для исследования набора данных MovieLens: оценок пользователей, фильмов, жанров, тегов, внешних ссылок и пользовательской активности. Результаты представлены в интерактивном отчёте Jupyter Notebook.

## Features
## Возможности

- Rating distribution and user activity analysis
- Top-rated, lowest-rated, and most-reviewed movies
- Genre and release-decade statistics
- Tag and external movie-link analysis
- Automated tests with pytest
- Interactive report with execution-time measurements
- Анализ распределения оценок и активности пользователей
- Поиск лучших, худших и самых популярных фильмов
- Статистика по жанрам и десятилетиям выпуска
- Анализ тегов и внешних ссылок на фильмы
- Автоматические тесты с использованием pytest
- Интерактивный отчёт с измерением времени выполнения

## Project Structure
## Структура проекта

```text
src/
├── movielens_analysis.py   # Analysis classes and methods
├── movielens_report.ipynb  # Jupyter Notebook report
├── test_movielens.py       # Automated tests
├── movielens_analysis.py   # Классы и методы анализа
├── movielens_report.ipynb  # Отчёт Jupyter Notebook
├── test_movielens.py       # Автоматические тесты
├── movies.csv
├── ratings.csv
├── tags.csv
└── links.csv
```

## Setup and Usage
## Установка и запуск

```bash
python3 -m venv venv
jupyter notebook movielens_report.ipynb
```

## Technologies
## Технологии

Python 3, Jupyter Notebook, pytest, and the MovieLens dataset.
Python 3, Jupyter Notebook, pytest и набор данных MovieLens.

## License
## Лицензия

This project is available under the MIT License.
Проект распространяется по лицензии MIT.
