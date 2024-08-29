#!/usr/bin/env python3
"""filter module"""

import re
from typing import List, Tuple
import logging
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """obfuscate log message"""
    return re.sub(f"({'|'.join(fields)})=([^ {separator}]*)",
                  f"\\1={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initiate object"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter log message"""
        msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """create logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    log_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    log_handler.setFormatter(formatter)

    return logger


def get_db() -> MySQLConnection:
    """establish database connection"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return conn


def main() -> None:
    """main function"""
    d_base = get_db()
    cursor = d_base.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    all_rows = cursor.fetchall()

    log = get_logger()
    for row in all_rows:
        message = "; ".join([f"{key}={value}" for key, value in row.items()])
        log.info(message)
    cursor.close()
    d_base.close()


if __name__ == "__main__":
    main()
