from app import app, USERS, POSTS, models
from flask import Response, request
import json
from http import HTTPStatus

@app.route("/")
def index():
    return "<h1>HI</h1>"

@app.post('/user/create')
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data['first_name']
    last_name = data['last_name']
    phone = data['phone']
    email = data['email']

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(id, first_name, last_name, phone, email)
    USERS.append(user)
    response = Response(
        json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "email": user.email,
            "total_reactions": "todo number",
            "posts": user.posts,
        }),
        HTTPStatus.OK,
        mimetype='application/json'
    )
    return response

@app.get('/user/<int:user_id>')
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "email": user.email,
            "total_reactions": "todo number",
            "posts": user.posts,
        }),
        HTTPStatus.OK,
        mimetype='application/json'
    )
    return response

@app.post('/posts/create')
def post_create():
    data = request.get_json()
    id = len(POSTS)
    author_id = data['author_id']
    text = data['text']
    if author_id < 0 or author_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = models.Post(id, author_id, text)
    POSTS.append(post)
    USERS[author_id].posts.append(id)
    response = Response(
        json.dumps({
        "id": post.id,
        "author_id": post.author_id,
        "text": post.text,
        "reactions" : post.reactions,
    }),
    HTTPStatus.OK,
    mimetype='application/json'
    )
    return response

@app.get('/posts/<int:post_id>')
def get_post(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]
    response = Response(
        json.dumps({
            "id": post.id,
            "author_id": post.author_id,
            "text": post.text,
            "reactions": post.reactions,
        }),
        HTTPStatus.OK,
        mimetype='application/json'
    )
    return response

@app.post('/posts/<int:post_id>/reaction')
def react(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    reaction = data["reaction"]
    if not reaction in ['like', 'fire', 'smile_emoji', 'crying_emoji', 'what_emoji']:
        return Response(status=HTTPStatus.NOT_FOUND)
    POSTS[post_id].reactions.append(reaction)
    response = Response(HTTPStatus.OK)
    return response

@app.get('/users/<int:user_id>/posts')
def sort_posts_by_reactions(user_id):
    if user_id < 0 or user_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    param = data['sort']
    if not (param == 'asc' or param == 'desc'):
        return Response(status=HTTPStatus.BAD_REQUEST)
    json_posts = USERS[user_id].sort_posts(param)

    response = Response(
        json.dumps({
            "posts": json_posts
        }),
        HTTPStatus.OK,
        mimetype='application/json'
    )
    return response


