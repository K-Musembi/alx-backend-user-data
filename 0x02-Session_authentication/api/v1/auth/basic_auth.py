#!/usr/bin/env python3
"""basic auth module"""

from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decode base64 value"""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decoded_value = base64.b64decode(base64_authorization_header)

            return decoded_value.decode("utf-8")
        except (UnicodeDecodeError, base64.binascii.Error):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """extract username and password"""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        email = ""
        password = ""
        semicolon = ""
        for char in decoded_base64_authorization_header:
            if char == ":":
                semicolon = char
            elif semicolon == "":
                email += char
            else:
                password += char

        if semicolon == "":
            return None, None

        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """retrieve user instance"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        if User.all():
            attribute_list = User.search({'email': user_email})
            if len(attribute_list) == 0:
                return None

            user_instance = attribute_list[0]
            if user_instance.is_valid_password(user_pwd) is False:
                return None

            return user_instance

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """complete basic auth operation"""
        auth_value = self.authorization_header(request)
        encoded_value = self.extract_base64_authorization_header(auth_value)
        decoded_value = self.decode_base64_authorization_header(encoded_value)
        credentials = self.extract_user_credentials(decoded_value)

        email, password = credentials
        user_instance = self.user_object_from_credentials(email, password)

        return user_instance
