from http import HTTPStatus
import requests

ENDPOINT = "http://127.0.0.1:5000"


def create_user_payload():
    return {
        "first_name": "Misha",
        "last_name": "Gorshenev",
        "phone": "89081234563",
        "email": "mishagorshok@ya.ru",
    }


def test_user_create():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["phone"] == payload["phone"]
    assert user_data["email"] == payload["email"]

    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")

    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["phone"] == payload["phone"]
    assert get_response.json()["email"] == payload["email"]


def test_user_create_wrong_data():
    payload_wrong_email = create_user_payload()
    payload_wrong_email["email"] = "mishagorshokya.ru"
    create_response = requests.post(
        f"{ENDPOINT}/users/create", json=payload_wrong_email
    )
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_repetitive_data():
    payload_rep_email = create_user_payload()
    payload_rep_email["phone"] = "89081234560"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload_rep_email)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        create_response.json()["ERROR"]
        == "User with these phone or email already exists"
    )

    payload_rep_phone = create_user_payload()
    payload_rep_phone["email"] = "mishagorshod@ya.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload_rep_phone)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        create_response.json()["ERROR"]
        == "User with these phone or email already exists"
    )


def test_sort_posts_by_reactions():
    payload = create_user_payload()
    payload["phone"] = "89082345678"
    payload["email"] = "mmmmmmmmm@bk.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]
    payload = {"sort": "asc"}
    get_response = requests.get(f"{ENDPOINT}/users/{user_id}/posts", json=payload)
    posts = get_response.json()["posts"]
    assert isinstance(posts, list)
    # todo test asc/desc sort


def test_get_users_leaderboard():
    payload = create_user_payload()
    payload["phone"] = "81112223334"
    payload["email"] = "mmmmmjjjjm@bk.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK

    payload = {"type": "list", "sort": "asc"}
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload)
    assert isinstance(get_response.json()["users"], list)

    payload = {"type": "graph"}
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload)
    print(get_response.text)
    assert get_response.text == ' <img src= "/static/images/users_leaderboard.png">'

    # todo test asc/desc sort
