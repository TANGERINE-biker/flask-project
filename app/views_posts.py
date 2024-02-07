from app import app, USERS, POSTS, models
from flask import Response, request
import json
from http import HTTPStatus


@app.post("/posts/create")
def post_create():
    data = request.get_json()
    id = len(POSTS)
    author_id = data["author_id"]
    text = data["text"]
    if author_id < 0 or author_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = models.Post(id, author_id, text)
    POSTS.append(post)
    USERS[author_id].posts.append(id)
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/posts/<int:post_id>/reaction")
def react(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)
    data = request.get_json()
    reaction = data["reaction"]
    reactions = ["like", "dislike", "fire", "smile_emoji", "crying_emoji", "what_emoji"]
    if not reaction in reactions:
        return Response(
            json.dumps({"ERROR": f"Please, use only {reactions} reactions"}),
            status=HTTPStatus.NOT_FOUND,
        )
    POSTS[post_id].reactions.append(reaction)
    response = Response(status=HTTPStatus.OK)
    return response
