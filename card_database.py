import mysql.connector
from database import get_connection


def get_or_create_set(set_name, set_code, set_year):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT Set_ID
            FROM MTG_Set
            WHERE Set_Code = %s
            """,
            (set_code,)
        )

        existing_set = cursor.fetchone()

        if existing_set is not None:
            return existing_set["Set_ID"]

        cursor.execute(
            """
            INSERT INTO MTG_Set (Set_Name, Set_Code, Set_Year)
            VALUES (%s, %s, %s)
            """,
            (set_name, set_code, set_year)
        )

        connection.commit()

        return cursor.lastrowid

    except mysql.connector.Error as error:
        if connection is not None:
            connection.rollback()

        print(error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def get_card(card_name, card_number, set_id, card_language):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM Card
            WHERE Card_Name = %s
              AND Card_Number = %s
              AND Set_ID = %s
              AND Card_Language = %s
            """,
            (card_name, card_number, set_id, card_language)
        )

        card = cursor.fetchone()

        return card

    except mysql.connector.Error as error:
        print(error)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def add_card(card_data, set_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            INSERT INTO Card (Card_Name,
                              Card_Number,
                              Colour_Identity,
                              Mana_Value,
                              Rarity,
                              Set_ID,
                              Card_Language,
                              Market_Price,
                              Foil_Market_Price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                card_data["name"],
                card_data["collector_number"],
                card_data["color_identity"],
                card_data["cmc"],
                card_data["rarity"],
                set_id,
                card_data["card_language"],
                card_data["market_price"],
                card_data["foil_market_price"]
            )
        )

        card_id = cursor.lastrowid

        for colour_code in card_data["colors"]:
            cursor.execute(
                """
                SELECT Colour_ID
                FROM Colour
                WHERE Colour_Code = %s
                """,
                (colour_code,)
            )

            colour = cursor.fetchone()

            if colour is None:
                continue

            cursor.execute(
                """
                INSERT INTO Card_Colour_Map (Card_ID, Colour_ID)
                VALUES (%s, %s)
                """,
                (card_id, colour["Colour_ID"])
            )

        for type_name in card_data["types"]:
            cursor.execute(
                """
                SELECT Type_ID
                FROM Type
                WHERE Type_Name = %s
                """,
                (type_name,)
            )

            card_type = cursor.fetchone()

            if card_type is None:
                cursor.execute(
                    """
                    INSERT INTO Type (Type_Name)
                    VALUES (%s)
                    """,
                    (type_name,)
                )

                type_id = cursor.lastrowid
            else:
                type_id = card_type["Type_ID"]

            cursor.execute(
                """
                INSERT INTO Card_Type_Map (Card_ID, Type_ID)
                VALUES (%s, %s)
                """,
                (card_id, type_id)
            )

        for subtype_name in card_data["subtypes"]:
            cursor.execute(
                """
                SELECT Subtype_ID
                FROM Subtype
                WHERE Subtype_Name = %s
                """,
                (subtype_name,)
            )

            card_subtype = cursor.fetchone()

            if card_subtype is None:
                cursor.execute(
                    """
                    INSERT INTO Subtype (Subtype_Name)
                    VALUES (%s)
                    """,
                    (subtype_name,)
                )

                subtype_id = cursor.lastrowid
            else:
                subtype_id = card_subtype["Subtype_ID"]

            cursor.execute(
                """
                INSERT INTO Card_Subtype_Map (Card_ID, Subtype_ID)
                VALUES (%s, %s)
                """,
                (card_id, subtype_id)
            )

        connection.commit()
        return card_id

    except mysql.connector.Error as error:
        if connection is not None:
            connection.rollback()

        print(error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()