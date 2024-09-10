#!/usr/bin/env python3
"""flask app module"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/")
def index():
    """home route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """register users"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = auth.register_user(email, password)
        if user:
            return jsonify({"email": email, "message": "user created"})
    except Exception as e:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """login the user"""
    email = request.form.get("email")
    password = request.form.get("password")

    if auth.valid_login(email, password) is False:
        abort(401)

    session_id = auth.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """delete session"""
    session_id = request.cookies.get("session_id")
    try:
        user = auth.get_user_from_session_id(session_id)
        if user:
            auth.destroy_session(user.id)
            return redirect("/")
    except Exception as e:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """retrieve user profile"""
    session_id = request.cookies.get("session_id")
    try:
        user = auth.get_user_from_session_id(session_id)
        if user is None:
            abort(403)

        return jsonify({"email": "<user email>"}), 200
    except Exception as e:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """reset user password"""
    email = request.form.get("email")
    try:
        reset_token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception as e:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """update user password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        auth.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
