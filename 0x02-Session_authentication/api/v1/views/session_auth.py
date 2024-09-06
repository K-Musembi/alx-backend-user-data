#!/usr/bin/env python3
"""session auth routes"""

from flask import jsonify, request, g, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route(
        "/auth_session/login", methods=['POST'], strict_slashes=False)
def session_route():
    """route for session auth"""
    from api.v1.app import auth

    email = request.form.get('email')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    attribute_list = User.search({'email': email})
    if len(attribute_list) == 0:
        return jsonify({"error": "no user found for this email"}), 400

    user_instance = attribute_list[0]

    if user_instance.is_valid_password(password) is False:
        return jsonify({"error": "wrong password"}), 404

    session_id = auth.create_session(user_instance.id)

    user_data = user_instance.to_json()

    response = jsonify(user_data)
    g.session_name = getenv('SESSION_NAME', session_id)
    response.set_cookie(g.session_name, session_id)

    return response


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def delete_session():
    """delete user session"""
    from api.v1.app import auth
    session_id = request.cookies.get(g.session_name)

    if auth.destroy_session(session_id) is False:
        abort(404)

    return jsonify({}), 200
