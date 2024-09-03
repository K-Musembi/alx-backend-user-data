#!/usr/bin/env python3
"""basic auth module"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """basic auth class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """base64 encoding"""
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        auth_type = ""
        value = ""
        count = 0
        for i in authorization_header:
            if count < 6:
                auth_type += i
                count += 1
            else:
                value += i

        if auth_type != "Basic ":
            return None

        return value
