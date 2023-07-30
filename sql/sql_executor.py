"""
Helper modules to execute sqlite scripts. 
"""
import sqlite3


def rabbitdb_executor():
    """
    Executes scripts on sqlite database.
    """

    conn = sqlite3.connect("data/rabbitdb.db")

    with conn:
        cur = conn.cursor()
        cur.executescript("thrifty_rabbit_schema.sql")


if __name__ == "__main__":
    rabbitdb_executor()
