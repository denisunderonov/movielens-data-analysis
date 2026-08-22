from datetime import datetime


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