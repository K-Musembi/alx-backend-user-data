#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User
from typing import Dict, Any

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """save user to database"""
        user = User(email=email, hashed_password=hashed_password)
        session = self.__session

        session.add(user)
        session.commit()

        return user

    def find_user_by(self, **kwargs: Dict[Any, Any]) -> User:
        """first row of users table"""
        session = self.__session
        try:
            user = session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise NoResultFound
            return user

        except InvalidRequestError as e:
            raise e
        finally:
            session.close()

    def update_user(self, user_id: int, **kwargs: Dict[str, Any]) -> None:
        """update user attributes"""
        user_session = self.__session

        try:
            user = self.find_user_by(id=user_id)
            for k, v in kwargs.items():
                if not hasattr(user, k):
                    raise ValueError
                setattr(user, k, v)
            user_session.commit()
        except Exception as e:
            raise e
        finally:
            user_session.close()
