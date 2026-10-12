import mysql.connector
from database import get_connection


def get_all_colours():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Colour ORDER BY Sort_Order")

        colours = cursor.fetchall()

        return colours

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def get_colour_by_code(colour_code):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM Colour WHERE Colour_Code = %s",
            (colour_code,)
        )

        colour = cursor.fetchone()

        return colour

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def add_card_colour(card_id, colour_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO Card_Colour_Map (Card_ID, Colour_ID)
            VALUES (%s, %s)
            """,
            (card_id, colour_id)
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


def get_colours_for_card(card_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT Colour.* "
                       "FROM Card_Colour_Map "
                       "JOIN Colour "
                       "ON Card_Colour_Map.Colour_ID = Colour.Colour_ID "
                       "WHERE Card_ID = %s "
                       "ORDER BY Colour.Sort_Order",
                       (card_id,))


        colours = cursor.fetchall()

        return colours

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()