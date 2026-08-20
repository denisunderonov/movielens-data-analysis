import csv
from datetime import datetime # Добавили импорт для работы с датой

class Tags:
    # Теперь класс принимает путь к файлу, как и Links!
    def __init__(self, file_path):
        self.data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for line in reader:
                tag_info = {
                    'userId': int(line['userId']),
                    'movieId': int(line['movieId']),
                    'tag': line['tag'],
                    'timestamp': int(line['timestamp'])
                }
                self.data.append(tag_info)

    def get_all(self):
        """Функция, которая возвращает весь файл"""
        return self.data
        
    # ИСПРАВЛЕНО: Теперь ищет все теги фильма и возвращает их с датами (sorted!)
    def get_tags_by_movie_with_dates(self, movie_id):
        """Возвращает список словарей {tag, timestamp, date} для фильма, отсортированный по времени."""
        result = []
        for line in self.data:
            if line['movieId'] == movie_id:
                # Превращаем timestamp (секунды с 1970 года) в читаемую дату
                date_str = datetime.fromtimestamp(line['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                result.append({
                    'tag': line['tag'],
                    'timestamp': line['timestamp'],
                    'date': date_str
                })
        # Сортируем по timestamp по возрастанию (от старых к новым)
        result.sort(key=lambda x: x['timestamp'])
        return result
    
    def get_tags_film(self, movie_id):
        """Возвращает просто список тегов для фильма"""
        tags = [] 
        for line in self.data:
            if line['movieId'] == movie_id:
                tags.append(line['tag'])
        return tags
    
    def get_tags_user(self, user_id): # Переименовал аргумент в user_id для логики
        """Возвращает список тегов, которые поставил конкретный пользователь"""
        tags = [] 
        for line in self.data:
            if line['userId'] == user_id:
                tags.append(line['tag'])
        return tags
        
    def get_most_popular_tags(self, n=10):
        """Возвращает топ-n самых популярных тегов (список кортежей)."""
        tag_counts = {}
        for row in self.data:
            tag = row['tag']
            if tag in tag_counts:
                tag_counts[tag] = tag_counts[tag] + 1
            else:
                tag_counts[tag] = 1
        
        # Превращаем словарь в список кортежей (tag, count)
        tags_list = []
        for tag, count in tag_counts.items():
            tags_list.append((tag, count))
            
        # Сортируем по убыванию количества (элемент с индексом 1 в кортеже)
        tags_list.sort(key=lambda x: x[1], reverse=True)
        return tags_list[:n]

    def get_unique_tags(self):
        """Возвращает отсортированный по алфавиту список уникальных тегов."""
        unique_tags = []
        for row in self.data:
            if row['tag'] not in unique_tags:
                unique_tags.append(row['tag'])
        unique_tags.sort() # Сортируем по алфавиту
        return unique_tags
    
    def get_unique_tags_count(self):
        """Возвращает количество уникальных тегов."""
        return len(self.get_unique_tags())
    
    def get_movies_by_tag(self, tag):
        """Возвращает отсортированный список movieId, к которым привязан указанный тег."""
        movie_ids = []
        for row in self.data:
            # lower() нужен, чтобы 'Funny' и 'funny' считались одним тегом
            if row['tag'].lower() == tag.lower():
                if row['movieId'] not in movie_ids:
                    movie_ids.append(row['movieId'])
        
        movie_ids.sort() # Сортируем по возрастанию ID
        return movie_ids
    
    def get_user_activity(self):
        """Возвращает список кортежей (userId, tags_count), отсортированный по убыванию."""
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
        """Возвращает общее количество записей тегов."""
        return len(self.data)