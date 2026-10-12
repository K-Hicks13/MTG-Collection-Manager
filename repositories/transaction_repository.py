import mysql.connector
from database import get_connection


def create_transaction_with_cursor(
    cursor,
    event_id,
    transaction_type
):
    cursor.execute("""INSERT INTO Collection_Transaction (Event_ID, Transaction_Type)
                      VALUES (%s, %s)
                   """,
                   (event_id, transaction_type)
                   )

    transaction_id = cursor.lastrowid

    return transaction_id


def create_transaction(event_id, transaction_type):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        transaction_id = create_transaction_with_cursor(cursor,
            event_id,
            transaction_type
            )

        connection.commit()
        return transaction_id

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


def add_transaction_item_with_cursor(
    cursor,
    transaction_id,
    card_id,
    direction,
    quantity,
    from_location_id,
    to_location_id,
    foil,
    card_condition,
    price_per_card,
    currency
):
    cursor.execute(
        """ INSERT INTO Collection_Transaction_Item (Transaction_ID, Card_ID, Direction, Quantity, From_Location_ID,
                                                     To_Location_ID, Foil, Card_Condition, Price_Per_Card, Currency)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   """,
                   (transaction_id, card_id, direction, quantity, from_location_id, to_location_id, foil, card_condition, price_per_card, currency)
                   )

    transaction_item_id = cursor.lastrowid
    return transaction_item_id


def add_transaction_item(
    transaction_id,
    card_id,
    direction,
    quantity,
    from_location_id,
    to_location_id,
    foil,
    card_condition,
    price_per_card,
    currency
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        transaction_item_id = add_transaction_item_with_cursor(
            cursor,
            transaction_id,
            card_id,
            direction,
            quantity,
            from_location_id,
            to_location_id,
            foil,
            card_condition,
            price_per_card,
            currency)

        connection.commit()
        return transaction_item_id

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


def get_transaction_items(transaction_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """ SELECT Collection_Transaction_Item.Transaction_Item_ID, 
                       Collection_Transaction_Item.Transaction_ID, 
                       Collection_Transaction_Item.Card_ID, 
                       Card.Card_Name, 
                       Collection_Transaction_Item.Direction, 
                       Collection_Transaction_Item.Quantity, 
                       Collection_Transaction_Item.From_Location_ID,
                       From_Location.Location_Name AS From_Location_Name,
                       Collection_Transaction_Item.To_Location_ID, 
                       To_Location.Location_Name AS To_Location_Name,
                       Collection_Transaction_Item.Foil, 
                       Collection_Transaction_Item.Card_Condition, 
                       Collection_Transaction_Item.Price_Per_Card, 
                       Collection_Transaction_Item.Currency
                FROM Collection_Transaction_Item
                JOIN Card 
                     ON Card.Card_ID = Collection_Transaction_Item.Card_ID
                LEFT JOIN Location AS From_Location
                          ON From_Location.Location_ID = Collection_Transaction_Item.From_Location_ID
                LEFT JOIN Location AS To_Location
                          ON To_Location.Location_ID = Collection_Transaction_Item.To_Location_ID
                WHERE Collection_Transaction_Item.Transaction_ID = %s
            """,
            (transaction_id,)
        )

        transaction_items = cursor.fetchall()
        return transaction_items

    except mysql.connector.Error as error:
        print(error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def get_transactions_for_event(event_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(""" SELECT * FROM Collection_Transaction
                           WHERE Event_ID = %s
                           ORDER BY Transaction_ID ASC
            """,
                (event_id,)
        )

        transaction_event = cursor.fetchall()
        return transaction_event

    except mysql.connector.Error as error:
        print(error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()