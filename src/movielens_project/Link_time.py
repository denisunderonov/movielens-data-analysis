import csv


class Links:

    def __init__(self):
        self.data=[]
        with open('links copy.csv','r') as file:
            reader=csv.DictReader(file)
            for line in reader:
                link={
                    'movieId':int(line['movieId']),
                    'imdbId':line['imdbId'],
                    'tmdbId':int(line['tmdbId'])
                }
                self.data.append(link)

    def get_all(self):
        """Функция, которая возвращает весь файл"""
        return self.data

    def get_link(self,movie_id):
        """Функция, которая принимает movieId, и возвращает значение  строки"""
        for line in self.data:
            if line['movieId']==movie_id:
                return line
        return None
        
    def get_only_imdbId(self, movie_id):
        """Возвращает только imdbId"""
        link=self.get_link(movie_id)
        return link['imdbId']

    def get_only_movieId(self, movie_id):
        """Возвращает только movieId"""
        link=self.get_link(movie_id)
        return link['movieId']

    def get_only_tmdbId(self, movie_id):
        """Возвращает только tmdbId"""
        link=self.get_link(movie_id)
        return link['tmdbId']

    def get_movielens_link(self, movie_id):
        """Возвращает ссылку на imdbId"""
        return f'https://movielens.org/movies/{movie_id}'

    def get_imdb_link(self, movie_id):
        """Возвращает ссылку на movieId"""
        id=self.get_only_imdbId(movie_id)
        return f'http://www.imdb.com/title/tt{id}/'

    def get_themoviedb_link(self, movie_id):
        """Возвращает ссылку на tmdbId"""
        id=self.get_only_tmdbId(movie_id)
        return f'https://www.themoviedb.org/movie/{id}'

    def get_count(self):
        """Возвращает длину"""
        return len(self.data) 

    def has_movie(self, movie_id):
        """Проверяет, есть ли такой movieId в базе. Возвращает True или False"""
        link = self.get_link(movie_id)
        if link is not None:
            return True
        return False
    
    
    def get_all_movie_ids(self):
        """Возвращает отсортированный список всех movieId"""
        ids = []
        for line in self.data:
            ids.append(line['movieId'])
        ids.sort() 
        return ids
    
    
obj=Links()
print(obj.get_all_movie_ids())
    