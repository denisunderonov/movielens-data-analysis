from collections import Counter
import re
from datetime import datetime

class Movies():
    def __init__(self):
        pass

    #Получает год из названия фильма
    def extract_year(self, title):
        match = re.search(r"\((\d{4})\)$", title)

        if match:
            return int(match.group(1))

        return None
    
    #Первоначальная обработка файла с фильмами
    def get_movies(self):
        result = {}
        is_first_line = True

        with open("movies.csv", "r", encoding="utf-8") as file:
            for line in file:
                if is_first_line:
                    is_first_line = False
                    continue

                line = line.strip()

                movie_id, remaining = line.split(",", 1)
                title, genres = remaining.rsplit(",", 1)

                title = title.strip('"')

                result[movie_id] = {
                    "title": title,
                    "genres": genres.split("|"),
                }

        return result

    #С помощью этого метода вытаскиваем всю важную информацию о фильме
    def get_all_films_information(self, ratings_list, movies_list):
        result = {}
        for movie in movies_list:
            result[movie] = {"title": movies_list[movie]["title"], 'ratings': [], "genres": movies_list[movie]["genres"], "year": self.extract_year(movies_list[movie]["title"])}

        #Добавление информации о рейтингах
        for item in ratings_list:
            result[item["movie_id"]]["ratings"].append(float(item["rating"]))

        #Рассчет и добавление информации о среднем рейтинге
        for film_id, film_info in result.items():
            if film_info["ratings"]:
                av_rating = sum(film_info["ratings"]) / len(film_info["ratings"])
            else:
                av_rating = None

            film_info["av_rating"] = av_rating
            film_info["reviews"] = len(film_info["ratings"])

        #Формируем Словарь из названий и среднего рейтинга и количества оценок
        films_list = {}
        for film_info in result.values():
            films_list[film_info["title"]] = {
            "av_rating": film_info["av_rating"],
            "reviews": film_info["reviews"],
            "genres": film_info["genres"],
            "year": film_info["year"]
        }

        #Сортируем по среднему рейтингу
        sorted_films = sorted(
            (
                item
                for item in films_list.items()
                if item[1]["av_rating"] is not None
            ),
            key=lambda item: item[1]["av_rating"],
            reverse=True,
        )

        return sorted_films

    def get_top_100_films(self, sorted_films):
        #Выбираем первую десятку фильмов, у которых более 20-ти оценок
        top_100 = []
        for film in sorted_films:
            if film[1]["reviews"] > 20:
                top_100.append(film)
            if len(top_100) == 100:
                break

        return top_100

    def get_worst_100_films(self, sorted_films):
        #Выбираем последнюю десятку фильмов, у которых более 20-ти оценок
        last_100 = []
        for film in reversed(sorted_films):
            if film[1]["reviews"] > 20:
                last_100.append(film)
            if len(last_100) == 100:
                break

        return last_100

    def get_top_genres(self, top_100):
        genres = Counter()
        for film in top_100:
            for genre in film[1]["genres"]:
                genres[genre] += 1
        top_10_genres = genres.most_common(10)

        return top_10_genres

    def get_worst_genres(self, last_100):
        genres = Counter()
        for film in last_100:
            for genre in film[1]["genres"]:
                genres[genre] += 1
        worst_10_genres = genres.most_common(10)

        return worst_10_genres

    def get_most_rev_films(self, sorted_films):
        popular_films = sorted(
            sorted_films,
            key=lambda film: film[1]["reviews"],
            reverse=True,
        )
        top_10 = popular_films[:10]

        return top_10

    def get_interesting_films(self, sorted_films):
        top = []
        for film in sorted_films[:1000]:
            if 5 <= film[1]["reviews"] and film[1]["reviews"] < 20:
                top.append(film)

        top_10 = top[:10]
        
        return top_10
       
    def get_av_genres_rating(self, sorted_films):
        genres = {}
        for film in sorted_films:
            for genre in film[1]["genres"]:
                genres[genre] = []
        for film in sorted_films:
            for genre in film[1]["genres"]:
                genres[genre].append(film[1]["av_rating"])

        average_genres = Counter()
        for genre, ratings in genres.items():
            average = sum(ratings) / len(ratings)
            average_genres[genre] = average

        return average_genres

    def get_year_analystics(self, sorted_films):
        years = {
            "40-е": {"ratings": [], "reviews": 0},
            "50-е": {"ratings": [], "reviews": 0},
            "60-е": {"ratings": [], "reviews": 0},
            "70-е": {"ratings": [], "reviews": 0},
            "80-е": {"ratings": [], "reviews": 0},
            "90-е": {"ratings": [], "reviews": 0},
            "2000-е": {"ratings": [], "reviews": 0},
            "2010-е": {"ratings": [], "reviews": 0},
            "2020-е": {"ratings": [], "reviews": 0},
        }

        for film in sorted_films:
            year = film[1]["year"]
            rating = film[1]["av_rating"]
            reviews = film[1]["reviews"]

            if year is None or rating is None:
                continue
            elif 1940 <= year <= 1949:
                decade = "40-е"
            elif 1950 <= year <= 1959:
                decade = "50-е"
            elif 1960 <= year <= 1969:
                decade = "60-е"
            elif 1970 <= year <= 1979:
                decade = "70-е"
            elif 1980 <= year <= 1989:
                decade = "80-е"
            elif 1990 <= year <= 1999:
                decade = "90-е"
            elif 2000 <= year <= 2009:
                decade = "2000-е"
            elif 2010 <= year <= 2019:
                decade = "2010-е"
            elif 2020 <= year <= 2029:
                decade = "2020-е"
            else:
                continue

            years[decade]["ratings"].append(rating)
            years[decade]["reviews"] += reviews

        result = {}

        for decade, info in years.items():
            if info["ratings"]:
                result[decade] = {
                    "av_rating": sum(info["ratings"]) / len(info["ratings"]),
                    "reviews": info["reviews"],
                    "films": len(info["ratings"]),
                }

        return result
    
class Ratings():
    def __init__(self):
        pass

    def get_ratings(self):
        result = []
        is_first_line = True

        with open('ratings.csv', "r", encoding="utf-8") as file:
            
            for line in file:
                if is_first_line:
                    is_first_line = False
                    continue
                split_line = line.split(',')
                item = {"user_id": split_line[0], "movie_id": split_line[1], "rating": split_line[2]}
                result.append(item)

        return result

    def get_sort_ratings(self, ratings):
        result = sorted(ratings, key=lambda item: float(item["rating"]), reverse=True)
        return result

    def sort_user(self, ratings):
        users_count = Counter(user["user_id"] for user in ratings)
        
        return users_count.most_common(10)
    
    #Считает количество каждого рейтинга
    def count_ratings(self, list):
        result = Counter(item["rating"] for item in list)
        
        return result
    
class Links:
    """Класс для работы с файлом links.csv. 
    Содержит связи между внутренними ID MovieLens и внешними базами (IMDb, TMDb)."""

    def __init__(self, file_path):
        """Инициализирует объект Links, читает файл и сохраняет данные в память."""
        self.data = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            for line in lines[1:]:
                parts = line.strip().split(',')
                
                if parts[2] == '':
                    tmdb_value = None
                else:
                    tmdb_value = int(parts[2])
                
                link = {
                    'movieId': int(parts[0]),
                    'imdbId': parts[1],
                    'tmdbId': tmdb_value
                }
                self.data.append(link)

    def get_all(self):
        """Возвращает список всех загруженных записей из файла links."""
        return self.data

    def get_link(self, movie_id):
        """Принимает movieId и возвращает словарь со всей информацией об этой ссылке.
        Если фильм не найден, возвращает None."""
        for line in self.data:
            if line['movieId'] == movie_id:
                return line
        return None
    
    def get_only_imdbId(self, movie_id):
        """Принимает movieId и возвращает только его imdbId (строку).
        Если фильм не найден, возвращает None."""
        link = self.get_link(movie_id)
        if link is not None:
            return link['imdbId']
        return None

    def get_only_movieId(self, movie_id):
        """Принимает movieId и возвращает его же (для проверки существования).
        Если фильм не найден, возвращает None."""
        link = self.get_link(movie_id)
        if link is not None:
            return link['movieId']
        return None

    def get_only_tmdbId(self, movie_id):
        """Принимает movieId и возвращает только его tmdbId (число или None).
        Если фильм не найден, возвращает None."""
        link = self.get_link(movie_id)
        if link is not None:
            return link['tmdbId']
        return None

    def get_movielens_link(self, movie_id):
        """Принимает movieId и возвращает готовую строку-ссылку на сайт MovieLens."""
        return f'https://movielens.org/movies/{movie_id}'

    def get_imdb_link(self, movie_id):
        """Принимает movieId и возвращает готовую строку-ссылку на сайт IMDb.
        Если фильм не найден, возвращает None."""
        imdb_id = self.get_only_imdbId(movie_id)
        if imdb_id is not None:
            return f'http://www.imdb.com/title/tt{imdb_id}/'
        return None

    def get_themoviedb_link(self, movie_id):
        """Принимает movieId и возвращает готовую строку-ссылку на сайт TheMovieDb.
        Если фильм не найден или у него нет tmdbId, возвращает None."""
        tmdb_id = self.get_only_tmdbId(movie_id)
        if tmdb_id is not None:
            return f'https://www.themoviedb.org/movie/{tmdb_id}'
        return None

    def get_count(self):
        """Возвращает общее количество записей (фильмов) в загруженном файле links."""
        return len(self.data)

    def get_all_movie_ids(self):
        """Возвращает отсортированный по возрастанию список всех movieId из файла."""
        ids = []
        for line in self.data:
            ids.append(line['movieId'])
        ids.sort()
        return ids

    def has_movie(self, movie_id):
        """Проверяет наличие фильма с заданным movieId в базе. 
        Возвращает True, если фильм есть, и False, если нет."""
        return self.get_link(movie_id) is not None


class Tags:
    """Класс для работы с файлом tags.csv. 
    Содержит пользовательские текстовые метки (теги), привязанные к фильмам."""

    def __init__(self, file_path):
        """Инициализирует объект Tags, читает файл и сохраняет данные в память."""
        self.data = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            for line in lines[1:]:
                parts = line.strip().split(',')
                tag_text = ','.join(parts[2:-1])
                
                tag_info = {
                    'userId': int(parts[0]),
                    'movieId': int(parts[1]),
                    'tag': tag_text,
                    'timestamp': int(parts[-1])
                }
                self.data.append(tag_info)

    def get_all(self):
        """Возвращает список всех загруженных записей тегов из файла."""
        return self.data
        
    def get_tags_by_movie_with_dates(self, movie_id):
        """Принимает movieId и возвращает список словарей с тегами этого фильма и их датами.
        Результат отсортирован по времени (timestamp) по возрастанию."""
        result = []
        for line in self.data:
            if line['movieId'] == movie_id:
                date_str = datetime.fromtimestamp(line['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                result.append({
                    'tag': line['tag'],
                    'timestamp': line['timestamp'],
                    'date': date_str
                })
        result.sort(key=lambda x: x['timestamp'])
        return result
    
    def get_tags_film(self, movie_id):
        """Принимает movieId и возвращает простой список строк (тегов) для этого фильма."""
        tags = [] 
        for line in self.data:
            if line['movieId'] == movie_id:
                tags.append(line['tag'])
        return tags
    
    def get_tags_user(self, user_id):
        """Принимает userId и возвращает список строк (тегов), которые оставил этот пользователь."""
        tags = [] 
        for line in self.data:
            if line['userId'] == user_id:
                tags.append(line['tag'])
        return tags
        
    def get_most_popular_tags(self, n=10):
        """Возвращает топ-n самых популярных тегов в виде списка кортежей (тег, количество).
        Результат отсортирован по убыванию популярности."""
        tag_counts = {}
        for row in self.data:
            tag = row['tag']
            if tag in tag_counts:
                tag_counts[tag] = tag_counts[tag] + 1
            else:
                tag_counts[tag] = 1
        
        tags_list = []
        for tag, count in tag_counts.items():
            tags_list.append((tag, count))
            
        tags_list.sort(key=lambda x: x[1], reverse=True)
        return tags_list[:n]

    def get_unique_tags(self):
        """Возвращает список всех уникальных тегов без повторений.
        Результат отсортирован по алфавиту."""
        unique_tags = []
        for row in self.data:
            if row['tag'] not in unique_tags:
                unique_tags.append(row['tag'])
        unique_tags.sort()
        return unique_tags
    
    def get_unique_tags_count(self):
        """Возвращает количество (число) уникальных тегов в датасете."""
        return len(self.get_unique_tags())
    
    def get_movies_by_tag(self, tag):
        """Принимает строку-тег и возвращает отсортированный по возрастанию список movieId,
        у которых есть этот тег."""
        movie_ids = []
        for row in self.data:
            if row['tag'].lower() == tag.lower():
                if row['movieId'] not in movie_ids:
                    movie_ids.append(row['movieId'])
        movie_ids.sort()
        return movie_ids
    
    def get_user_activity(self):
        """Возвращает список кортежей (userId, количество_тегов) для всех пользователей.
        Результат отсортирован по убыванию активности (количеству тегов)."""
        user_counts = {}
        for row in self.data:
            uid = row['userId']
            if uid in user_counts:
                user_counts[uid] = user_counts[uid] + 1
            else:
                user_counts[uid] = 1
                
        users_list = []
        for uid, count in user_counts.items():
            users_list.append((uid, count))
            
        users_list.sort(key=lambda x: x[1], reverse=True)
        return users_list
    
    def get_tags_count(self):
        """Возвращает общее количество записей (строк) в загруженном файле tags."""
        return len(self.data)
