from app import app, USERS, POSTS, models
from flask import Response, request, url_for
import json
from http import HTTPStatus
import matplotlib.pyplot as plt


@app.route("/")
def index():
    return "<h1>HI</h1>"


@app.post("/users/create")
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    email = data["email"]
    for user in USERS:
        if user.phone == phone or user.email == email:
            return Response(
                json.dumps({"ERROR": "User with these phone or email already exists"}),
                status=HTTPStatus.BAD_REQUEST,
                mimetype="application/json",
            )
    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(id, first_name, last_name, phone, email)
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "total_reactions": user.total_reactions(),
                "posts": user.posts,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "total_reactions": user.total_reactions(),
                "posts": user.posts,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>/posts")
def sort_posts_by_reactions(user_id):
    if user_id < 0 or user_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    param = data["sort"]
    if not (param == "asc" or param == "desc"):
        return Response(status=HTTPStatus.BAD_REQUEST)
    json_posts = USERS[user_id].sort_posts(param)

    response = Response(
        json.dumps({"posts": json_posts}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def leaderboard():
    data = request.get_json()
    type = data["type"]
    if not (type == "list" or type == "graph"):
        return Response(status=HTTPStatus.BAD_REQUEST)
    if type == "list":
        param = data["sort"]
        if not (param == "asc" or param == "desc"):
            return Response(status=HTTPStatus.BAD_REQUEST)
        json_ldbrd = models.sort_users(USERS, param)
        response = Response(
            json.dumps({"users": json_ldbrd}),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )
        return response

    elif type == "graph":
        USERS.sort(key=lambda x: x.total_reactions(), reverse=True)
        fig, ax = plt.subplots()
        user_data = [
            f"{user.first_name} {user.last_name} ID: {user.id}" for user in USERS
        ]
        user_reactions = [user.total_reactions() for user in USERS]
        ax.bar(user_data, user_reactions)
        ax.set_ylabel("Total reactions")
        ax.set_title("User leaderboard by total reactions")
        plt.savefig("app/static/images/users_leaderboard.png")
        return Response(
            f""" <img src= "{url_for('static', filename='images/users_leaderboard.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )

    else:
        return Response(status=HTTPStatus.BAD_REQUEST)
