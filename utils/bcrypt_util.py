# -*- coding: utf-8 -*-
"""
bcrypt_util.py
"""

import bcrypt


def encode_password(password: str) -> str:
    """
    加密过程
    :param password: str
    :return: str
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def check_password(password: str, hashed_password: str) -> bool:
    """
    校验过程
    :param password: str
    :param hashed_password: str
    :return: bool
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

