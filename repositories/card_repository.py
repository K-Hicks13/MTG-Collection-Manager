import mysql.connector
from database import get_connection


def get_all_cards():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT Card.*, MTG_Set.Set_Name, MTG_Set.Set_Code "
                       "FROM Card "
                       "JOIN MTG_Set "
                       "ON Card.Set_ID = MTG_Set.Set_ID ")

        cards = cursor.fetchall()

        return cards

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def add_card(card_name, card_number, colour_identity, mana_value, rarity, set_id, card_language, market_price=None, foil_market_price=None):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO Card (Card_Name, Card_Number, Colour_Identity, Mana_Value, Rarity, Set_ID, Card_Language, Market_Price, Foil_Market_Price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (card_name, card_number, colour_identity, mana_value, rarity, set_id, card_language, market_price, foil_market_price)
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


def get_card_by_id(card_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT Card.*, MTG_Set.Set_Name, MTG_Set.Set_Code "
                       "FROM Card "
                       "JOIN MTG_Set "
                       "ON Card.Set_ID = MTG_Set.Set_ID "
                       "WHERE Card.Card_ID = %s",
                       (card_id,))

        card = cursor.fetchone()

        return card

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def get_card_by_printing(card_name, card_number, set_id, card_language):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT Card.*, MTG_Set.Set_Name, MTG_Set.Set_Code "
                       "FROM Card "
                       "JOIN MTG_Set "
                       "ON Card.Set_ID = MTG_Set.Set_ID "
                       "WHERE Card.Card_Name = %s AND Card.Card_Number = %s AND Card.Set_ID = %s AND Card.Card_Language = %s",
                       (card_name, card_number, set_id, card_language))

        card = cursor.fetchone()

        return card

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()