from collections import Counter
import re

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
