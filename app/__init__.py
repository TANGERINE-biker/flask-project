from flask import Flask

app = Flask(__name__)

USERS = []  # list of type User
POSTS = []  # list of type Post

from app import views
from app import models
