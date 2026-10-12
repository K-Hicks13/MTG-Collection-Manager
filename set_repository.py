import mysql.connector
from database import get_connection


def get_all_sets():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM MTG_Set")

        sets = cursor.fetchall()

        return sets

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def add_set(set_name, set_code, set_year):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO MTG_Set (Set_Name, Set_Code, Set_Year)
            VALUES (%s, %s, %s)
            """,
            (set_name, set_code, set_year)
        )

        connection.commit()
        return True

    except mysql.connector.Error as error:
        print(error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def get_set_by_id(set_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM MTG_Set WHERE Set_ID = %s",
            (set_id,)
        )

        mtg_set = cursor.fetchone()

        return mtg_set

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def get_set_by_code(set_code):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM MTG_Set WHERE Set_Code = %s",
            (set_code,)
        )

        mtg_set = cursor.fetchone()

        return mtg_set

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()