from app import app, USERS, POSTS, models
from flask import Response, request
import json
from http import HTTPStatus
import requests

ENDPOINT = "http://127.0.0.1:5000"


def create_user_payload():
    return {
        "first_name": "Misha",
        "last_name": "Gorshenev",
        "phone": "89080000000",
        "email": "mikhailgorshenev@ya.ru",
    }


def create_post_payload():
    return {"author_id": 0, "text": "А муха тоже вертолет...."}


def test_posts_create():
    payload = create_user_payload()
    create_user_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_user_response.status_code == HTTPStatus.OK
    payload = create_post_payload()

    create_post_response = requests.post(f"{ENDPOINT}/posts/create", json=payload)
    assert create_post_response.status_code == HTTPStatus.OK
    post_data = create_post_response.json()
    post_id = post_data["id"]
    assert post_data["author_id"] == payload["author_id"]
    assert post_data["text"] == payload["text"]

    get_post_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
    assert get_post_response.json()["author_id"] == payload["author_id"]
    assert get_post_response.json()["text"] == payload["text"]


def test_posts_react():
    payload = create_user_payload()
    payload["phone"] = "89080000001"
    payload["email"] = "mikhailgorshenev@gmail.com"
    create_user_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_user_response.status_code == HTTPStatus.OK
    payload = create_post_payload()

    create_post_response = requests.post(f"{ENDPOINT}/posts/create", json=payload)
    assert create_post_response.status_code == HTTPStatus.OK
    post_data = create_post_response.json()
    post_id = post_data["id"]

    reaction = {"reaction": "fire"}
    react_post_response = requests.post(
        f"{ENDPOINT}/posts/{post_id}/reaction", json=reaction
    )
    assert react_post_response.status_code == HTTPStatus.OK

    get_post_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
    assert get_post_response.json()["author_id"] == payload["author_id"]
    assert get_post_response.json()["text"] == payload["text"]
    assert isinstance(get_post_response.json()["reactions"], list)
    assert "fire" in get_post_response.json()["reactions"]
    assert len(get_post_response.json()["reactions"]) == 1
