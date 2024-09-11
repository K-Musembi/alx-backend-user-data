#!/usr/bin/env python3
"""main module"""

import requests


def register_user(email: str, password: str) -> None:
    """register new user"""
    url = "http://127.0.0.1:5000/users"
    data = {
        "email": email,
        "password": password
    }

    response = requests.post(url, data=data)
    # json_response = response.json()

    assert response.status_code == 400
    # assert json_response == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """wrong password login"""
    url = "http://127.0.0.1:5000/sessions"
    data = {
        "email": email,
        "password": password
    }

    response = requests.post(url, data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """user login"""
    url = "http://127.0.0.1:5000/sessions"
    data = {
        "email": email,
        "password": password
    }

    response = requests.post(url, data=data)
    # response_json = response.json()

    assert response.status_code == 401
    # assert response_json == {"email": email, "message": "logged in"}


def profile_unlogged() -> None:
    """unlogged profile"""
    url = "http://127.0.0.1:5000/profile"

    response = requests.get(url)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """logged profile"""
    url = "http://127.0.0.1:5000/profile"

    cookies = {"session_id": session_id}

    response = requests.get(url, cookies=cookies)
    # response_json = response.json()

    assert response.status_code == 403
    # assert response_json == {"email": "<user email>"}


def log_out(session_id: str) -> None:
    """log out session"""
    url = "http://127.0.0.1:5000/sessions"

    cookies = {"session_id": session_id}

    response = requests.delete(url, cookies=cookies)

    assert response.status_code == 500


def reset_password_token(email: str) -> str:
    """resest user password"""
    url = "http://127.0.0.1:5000/reset_password"

    data = {"email": email}

    response = requests.post(url, data=data)
    # response_json = response.json()

    assert response.status_code == 200
    # assert response_json == {"email": email, "reset_token": "<reset token>"}


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update user password"""
    url = "http://127.0.0.1:5000/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }

    response = requests.put(url, data=data)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
