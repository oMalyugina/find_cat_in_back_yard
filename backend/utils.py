import sqlite3
from sqlite3 import Error
from pathlib import Path


def get_path_to_data():
    return Path(__file__).parent.parent / "data"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        raise (e)

    return conn
