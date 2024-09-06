#!/usr/bin/env python3
"""auth API module"""

from flask import request
from typing import List, TypeVar
from models.user import User
from os import getenv


class Auth:
    """auth API class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return true if path not excluded"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        normalized_list = [pathstr.rstrip("/") for pathstr in excluded_paths]
        normalized_path = path.rstrip("/")

        if normalized_path in normalized_list:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """auth header"""
        if request is None:
            return None

        auth = request.headers.get("Authorization")
        if auth is None:
            return None

        return auth

    def current_user(self, request=None) -> User:
        """user object"""
        return None

    def session_cookie(self, request=None):
        """request cookie value"""
        if request is None:
            return None

        _my_session_id = getenv('SESSION_NAME')
        cookie_value = request.cookies.get(_my_session_id)

        return cookie_value
