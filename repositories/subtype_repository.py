import mysql.connector
from database import get_connection


def get_subtype_by_name(subtype_name):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM Subtype WHERE Subtype_Name = %s",
            (subtype_name,)
        )

        card_subtype = cursor.fetchone()

        return card_subtype

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def add_subtype(subtype_name):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO Subtype (Subtype_Name)
            VALUES (%s)
            """,
            (subtype_name,)
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


def add_card_subtype(card_id, subtype_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO Card_Subtype_Map (Card_ID, Subtype_ID)
            VALUES (%s, %s)
            """,
            (card_id, subtype_id)
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


def get_subtypes_for_card(card_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT Subtype.* "
                       "FROM Card_Subtype_Map "
                       "JOIN Subtype "
                       "ON Card_Subtype_Map.Subtype_ID = Subtype.Subtype_ID "
                       "WHERE Card_ID = %s ",
                       (card_id,))

        subtypes = cursor.fetchall()

        return subtypes

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()