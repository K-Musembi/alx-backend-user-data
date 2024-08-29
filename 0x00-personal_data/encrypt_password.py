#!/usr/bin/env python3
"""encrypt user passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """ecryption function"""
    salt = bcrypt.gensalt()
    encrypted = bcrypt.hashpw(password.encode(), salt)
    return encrypted


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate hash operation"""
    return bcrypt.checkpw(password.encode(), hashed_password)
