import re
from app import POSTS


class User:
    def __init__(self, id, first_name, last_name, phone, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.posts = []

    @staticmethod
    def is_valid_email(email):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if re.fullmatch(regex, email):
            return True
        return False

    def sort_posts(self, param):
        if param == "asc":
            self.posts.sort(key=lambda x: len(POSTS[x].reactions))
        if param == "desc":
            self.posts.sort(key=lambda x: len(POSTS[x].reactions), reverse=True)

        json_posts = []
        for id in self.posts:
            json_posts.append(
                {
                    "id": id,
                    "author_id": POSTS[id].author_id,
                    "text": POSTS[id].text,
                    "reactions": POSTS[id].reactions,
                }
            )
        return json_posts

    def total_reactions(self):
        total = sum([len(POSTS[id].reactions) for id in self.posts])
        return total


class Post:
    def __init__(self, id, author_id, text):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.reactions = []


def sort_users(USERS, param):
    if param == "asc":
        USERS.sort(key=lambda x: x.total_reactions())
    if param == "desc":
        USERS.sort(key=lambda x: x.total_reactions(), reverse=True)

    json_ldbrd = []
    for user in USERS:
        json_ldbrd.append(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "total_reactions": user.total_reactions(),
                "posts": user.posts,
            }
        )
    return json_ldbrd
