from flask import Flask

app = Flask(__name__)

USERS = []  # list of type User
POSTS = []  # list of type Post

from app import views_users
from app import views_posts
from app import models
