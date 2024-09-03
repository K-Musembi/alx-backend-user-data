#!/usr/bin/env python3
"""auth API module"""

from flask import request
from typing import List, TypeVar
from models.user import User


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
        return auth

    def current_user(self, request=None) -> User:
        """user object"""
        return None
