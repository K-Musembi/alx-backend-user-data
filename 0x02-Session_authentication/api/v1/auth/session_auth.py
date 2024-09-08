#!/usr/bin/env python3
"""session auth module"""

from api.v1.auth.auth import Auth
import uuid

from models.user import User


class SessionAuth(Auth):
    """session auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create sssion for user id"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id.update({session_id: user_id})

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return user id"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """current user id"""
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """delete user session"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id['session_id']

        return True
