#!/usr/bin/env python3
"""encryption module"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """encryption function"""
    salt = bcrypt.gensalt()
    encrypted = bcrypt.hashpw(password.encode('utf-8'), salt)

    return encrypted


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register new user"""
        try:
            new_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")

        except NoResultFound:
            encrypted = _hash_password(password)
            new_user = self._db.add_user(email, encrypted)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """validate credentials"""
        try:
            new_user = self._db.find_user_by(email=email)

            if new_user:
                encrypted = _hash_password(password)
                if bcrypt.checkpw(
                        password.encode('utf-8'), encrypted.encode('utf-8')):
                    return True
        except Exception as e:
            return False

        return False

    def _generate_uuid(self) -> str:
        """generate string uuid"""
        string_uuid = str(uuid.uuid4())

        return string_uuid

    def create_session(self, email: str) -> str:
        """create session id"""
        try:
            user = self._db.find_user_by(email=email)
            user_id = user.id
            session_id = self._generate_uuid()
            self._db.update_user(user_id, session_id=session_id)
            return session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """retrieve corresponding user"""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """cancel user session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except Exception as e:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """password reset"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                string_uuid = self._generate_uuid()
                self._db.update_user(user.id, reset_token=string_uuid)
                return string_uuid
        except Exception as e:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """update user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                encrypted = _hash_password(password)
                self._db.update_user(user.id, hashed_password=encrypted,
                                     reset_token=None)
        except Exception as e:
            raise ValueError
