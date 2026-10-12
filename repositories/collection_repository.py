import mysql.connector
from database import get_connection


def get_all_collection_entries():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT Collection.*, Card.Card_Name, Card.Card_Number, Location.Location_Name "
                       "FROM Collection "
                       "JOIN Card "
                       "ON Collection.Card_ID = Card.Card_ID "
                       "JOIN Location "
                       "ON Collection.Location_ID = Location.Location_ID "
                       "WHERE Collection.Is_Deleted = 0")

        collection = cursor.fetchall()

        return collection

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def get_collection_entry(card_id, location_id, foil, card_condition):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT Collection.* "
                       "FROM Collection "
                       "WHERE Card_ID = %s AND Location_ID = %s AND Foil = %s AND Card_Condition = %s",
                       (card_id, location_id, foil, card_condition))

        collection_entry = cursor.fetchone()

        return collection_entry

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()



def remove_from_collection_with_cursor(
    cursor,
    collection_id,
    quantity_to_remove
):
    if quantity_to_remove <= 0:
        return False

    cursor.execute(
        """
        SELECT *
        FROM Collection
        WHERE Collection_ID = %s
          AND Is_Deleted = 0
        """,
        (collection_id,))

    collection_entry = cursor.fetchone()

    if collection_entry is None:
        return False

    if quantity_to_remove < collection_entry["Quantity"]:
        cursor.execute("UPDATE Collection "
                       "SET Quantity = Quantity - %s "
                       "WHERE Collection_ID = %s",
                       (quantity_to_remove, collection_id)
                       )
    elif quantity_to_remove == collection_entry["Quantity"]:
        cursor.execute("UPDATE Collection "
                       "SET Is_Deleted = 1 "
                       "WHERE Collection_ID = %s",
                       (collection_id,))

    else:
        return False

    return True


def remove_from_collection(collection_id, quantity_to_remove):
    if quantity_to_remove <= 0:
        return False

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        result = remove_from_collection_with_cursor(
            cursor,
            collection_id,
            quantity_to_remove
        )

        if result is False:
            return False

        connection.commit()
        return True

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


def add_to_collection_with_cursor(
    cursor,
    card_id,
    location_id,
    quantity,
    foil,
    card_condition
):
    if quantity <= 0:
        return False

    cursor.execute("SELECT Collection.* "
                   "FROM Collection "
                   "WHERE Card_ID = %s AND Location_ID = %s AND Foil = %s AND Card_Condition = %s",
                   (card_id, location_id, foil, card_condition))

    existing_entry = cursor.fetchone()

    if existing_entry is None:
        cursor.execute(
            """
            INSERT INTO Collection (Card_ID, Location_ID, Quantity, Foil, Card_Condition)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (card_id, location_id, quantity, foil, card_condition)
        )
    elif existing_entry["Is_Deleted"] == 0:
        cursor.execute(
              """
             UPDATE Collection
              SET Quantity = Quantity + %s
              WHERE Collection_ID = %s
              """,
              (quantity, existing_entry["Collection_ID"])
         )
    else:
         cursor.execute(
              """
              UPDATE Collection
               SET Quantity   = %s,
                   Is_Deleted = 0
               WHERE Collection_ID = %s
                 AND Is_Deleted = 1
               """,
            (quantity, existing_entry["Collection_ID"])
         )

    return True


def add_to_collection(card_id, location_id, quantity, foil, card_condition):
    if quantity <= 0:
        return False

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        result = add_to_collection_with_cursor(
            cursor,
            card_id,
            location_id,
            quantity,
            foil,
            card_condition
        )

        if result is False:
            return False

        connection.commit()
        return True

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


def get_collection_details():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
                       SELECT Collection.Collection_ID, 
                              Card.Card_Name, 
                              COALESCE(GROUP_CONCAT(Colour.Colour_Code ORDER BY Colour.Sort_Order SEPARATOR ' '), 'C') AS Colour, 
                              Card.Mana_Value, 
                              MTG_Set.Set_Name, 
                              Location.Location_Name, 
                              Collection.Quantity, 
                              Collection.Foil, 
                              Collection.Card_Condition
                       FROM Collection 
                        JOIN Card 
                             ON Collection.Card_ID = Card.Card_ID
                        JOIN MTG_Set 
                             ON Card.Set_ID = MTG_Set.Set_ID
                        JOIN Location 
                             ON Collection.Location_ID = Location.Location_ID
                        LEFT JOIN Card_Colour_Map 
                             ON Card.Card_ID = Card_Colour_Map.Card_ID
                        LEFT JOIN Colour 
                             ON Colour.Colour_ID = Card_Colour_Map.Colour_ID
                        WHERE Collection.Is_Deleted = 0
                        GROUP BY Collection.Collection_ID
                       """)

        collection = cursor.fetchall()

        return collection

    except mysql.connector.Error as error:
        print(error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def increase_collection_quantity(collection_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM Collection
            WHERE Collection_ID = %s
              AND Is_Deleted = 0
            """,
            (collection_id,))

        collection_entry = cursor.fetchone()

        if collection_entry is None:
            return False

        cursor.execute("UPDATE Collection "
                       "SET Quantity = Quantity + 1 "
                       "WHERE Collection_ID = %s",
                       (collection_id,)
                       )

        connection.commit()
        return True

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


def get_collection_entry_details(collection_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
                       SELECT Collection.Collection_ID,
                              Card.Card_Name,
                              Card.Card_Number,
                              MTG_Set.Set_Name,
                              COALESCE(GROUP_CONCAT(DISTINCT Colour.Colour_Code ORDER BY Colour.Sort_Order SEPARATOR ' '), 'C') AS Colour,
                              Card.Colour_Identity,
                              GROUP_CONCAT(DISTINCT Type.Type_Name ORDER BY FIELD(Type.Type_Name,
                                                                    'Legendary',
                                                                    'Basic',
                                                                    'Snow',
                                                                    'World',
                                                                    'Ongoing',
                                                                    'Artifact',
                                                                    'Enchantment',
                                                                    'Creature',
                                                                    'Planeswalker',
                                                                    'Battle',
                                                                    'Instant',
                                                                    'Sorcery',
                                                                    'Kindred',
                                                                    'Land') SEPARATOR ' ') AS Types,
                              GROUP_CONCAT(DISTINCT Subtype.Subtype_Name SEPARATOR ' ') AS Subtypes,
                              Card.Mana_Value,
                              Card.Rarity,
                              Card.Card_Language,
                              Card.Market_Price,
                              Card.Foil_Market_Price,
                              Location.Location_Name,
                              Collection.Quantity,
                              Collection.Foil,
                              Collection.Card_Condition
                       FROM Collection
                            JOIN Card
                                 ON Collection.Card_ID = Card.Card_ID
                            JOIN MTG_Set
                                 ON Card.Set_ID = MTG_Set.Set_ID
                            JOIN Location
                                 ON Collection.Location_ID = Location.Location_ID
                            LEFT JOIN Card_Colour_Map
                                 ON Card.Card_ID = Card_Colour_Map.Card_ID
                            LEFT JOIN Colour 
                                 ON Colour.Colour_ID = Card_Colour_Map.Colour_ID
                            LEFT JOIN Card_Type_Map
                                 ON Card.Card_ID = Card_Type_Map.Card_ID
                            LEFT JOIN Type 
                                 ON Type.Type_ID = Card_Type_Map.Type_ID
                            LEFT JOIN Card_Subtype_Map
                                 ON Card.Card_ID = Card_Subtype_Map.Card_ID
                            LEFT JOIN Subtype 
                                 ON Subtype.Subtype_ID = Card_Subtype_Map.Subtype_ID
                       WHERE Collection.Is_Deleted = 0 AND Collection.Collection_ID = %s
                       GROUP BY Collection.Collection_ID
                       """,
                       (collection_id,))

        collection = cursor.fetchone()
        return collection

    except mysql.connector.Error as error:
        print(error)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def update_collection_entry(collection_id, location_id, quantity, foil, card_condition):
    if quantity <= 0:
        return False

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        result = update_collection_entry_with_cursor(
            cursor,
            collection_id,
            location_id,
            quantity,
            foil,
            card_condition
        )

        if result is False:
            connection.rollback()
            return False

        connection.commit()
        return True

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


def remove_collection_entry(collection_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""SELECT * FROM Collection 
                          WHERE Collection_ID = %s AND Is_Deleted = 0
        """,
            (collection_id,)
        )

        collection_entry = cursor.fetchone()

        if collection_entry is None:
            return False

        cursor.execute("""UPDATE Collection
                          SET Is_Deleted = 1
                          WHERE Collection_ID = %s AND Is_Deleted = 0
        """,
                   (collection_id,)
        )

        connection.commit()
        return True

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


def update_collection_entry_with_cursor(
    cursor,
    collection_id,
    location_id,
    quantity,
    foil,
    card_condition
):
    if quantity <= 0:
        return False

    cursor.execute(
        """
        SELECT *
        FROM Collection
        WHERE Collection_ID = %s
          AND Is_Deleted = 0
        """,
        (collection_id,)
    )

    existing_entry = cursor.fetchone()

    if existing_entry is None:
        return False

    cursor.execute(
        """
        SELECT *
        FROM Collection
        WHERE Card_ID = %s
          AND Location_ID = %s
          AND Foil = %s
          AND Card_Condition = %s
        """,
        (
            existing_entry["Card_ID"],
            location_id,
            foil,
            card_condition
        )
    )

    matching_entry = cursor.fetchone()

    if matching_entry is None:
        cursor.execute(
            """
            UPDATE Collection
            SET Location_ID    = %s,
                Quantity       = %s,
                Foil           = %s,
                Card_Condition = %s
            WHERE Collection_ID = %s
            """,
            (location_id, quantity, foil, card_condition, collection_id)
        )

    elif matching_entry["Collection_ID"] == existing_entry["Collection_ID"]:
        cursor.execute(
            """
            UPDATE Collection
            SET Quantity = %s
            WHERE Collection_ID = %s
            """,
            (quantity, collection_id)
        )

    else:
        if matching_entry["Is_Deleted"] == 1:
            cursor.execute("""UPDATE Collection
                              SET Quantity   = %s,
                                  Is_Deleted = 0
                              WHERE Collection_ID = %s
                           """,
                           (quantity, matching_entry["Collection_ID"])
                           )

            cursor.execute("""UPDATE Collection
                              SET Is_Deleted = 1
                              WHERE Collection_ID = %s
                           """,
                           (collection_id,)
                           )

        else:
            cursor.execute("""UPDATE Collection
                              SET Quantity = Quantity + %s
                              WHERE Collection_ID = %s
                           """,
                           (quantity, matching_entry["Collection_ID"])
                           )

            cursor.execute("""UPDATE Collection
                              SET Is_Deleted = 1
                              WHERE Collection_ID = %s
                           """,
                           (collection_id,)
                           )

    return True