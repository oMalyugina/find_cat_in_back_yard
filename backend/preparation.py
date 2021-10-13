import sqlite3
from sqlite3 import Error

from utils import get_path_to_data, create_connection



def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """

    create_table_sql = """ CREATE TABLE IF NOT EXISTS projects (
                                            id_frame text  PRIMARY KEY,
                                            id_on_frame integer NOT NULL,
                                            x integer NOT NULL,
                                            y integer NOT NULL,
                                            w integer NOT NULL,
                                            h integer NOT NULL
                                        ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except:
        raise Exception("can't create sqlite database")


if __name__ == "__main__":
    database = get_path_to_data() / "processed" / "results.db"
    conn = create_connection(database)
    create_table(conn)
