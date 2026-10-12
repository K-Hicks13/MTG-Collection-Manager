import mysql.connector
from database import get_connection


def get_type_by_name(type_name):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM Type WHERE Type_Name = %s",
            (type_name,)
        )

        card_type = cursor.fetchone()

        return card_type

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def add_type(type_name):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO Type (Type_Name)
            VALUES (%s)
            """,
            (type_name,)
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


def add_card_type(card_id, type_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO Card_Type_Map (Card_ID, Type_ID)
            VALUES (%s, %s)
            """,
            (card_id, type_id)
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


def get_types_for_card(card_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT Type.* "
                       "FROM Card_Type_Map "
                       "JOIN Type "
                       "ON Card_Type_Map.Type_ID = Type.Type_ID "
                       "WHERE Card_ID = %s ",
                       (card_id,))

        types = cursor.fetchall()

        return types

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()