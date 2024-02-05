#models.py
import re
from app import POSTS
class User:
#      todo проверка почты на правильность,
#       может писать посты, ставить реакции (heart, like, dislike, boom)
#       на посты других пользователей

    def __init__(self, id, first_name, last_name, phone, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.posts = []

    @staticmethod
    def is_valid_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (re.fullmatch(regex, email)):
            return True
        return False

    def sort_posts(self, param):# User.posts.sort(key= lambda x: POSTS[x].length)
        if param == 'asc':
            self.posts.sort(key=lambda x: len(POSTS[x].reactions))
        if param == 'desc':
            self.posts.sort(key=lambda x: len(POSTS[x].reactions), reverse=True)

        json_posts = []
        for id in self.posts:
            json_posts.append({
                "id": id,
                "author_id": POSTS[id].author_id,
                "text": POSTS[id].text,
                "reactions": POSTS[id].reactions,
            })
        return json_posts


class Post:
    def __init__(self,id, author_id, text):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.reactions = []

    #       todo имеет методы создания поста:
    #        содержит текст поста, реакции из списка

