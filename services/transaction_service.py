import mysql.connector

from database import get_connection
from repositories.transaction_repository import create_transaction_with_cursor
from repositories.transaction_repository import add_transaction_item_with_cursor
from repositories.collection_repository import add_to_collection_with_cursor
from repositories.collection_repository import remove_from_collection_with_cursor
from repositories.collection_repository import update_collection_entry_with_cursor
from repositories.event_repository import create_event_with_cursor

def add_cards_with_transaction(
    event_date,
    transaction_type,
    person_place,
    notes,
    card_id,
    location_id,
    quantity,
    foil,
    card_condition,
    price_per_card,
    currency
):
    allowed_in_types = [
        "Purchase",
        "Trade",
        "Gift",
        "Initial Inventory",
        "Other"
    ]

    if transaction_type not in allowed_in_types:
        return False

    if quantity < 1:
        return False

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        event_id = create_event_with_cursor(
            cursor,
            event_date,
            "Add",
            person_place,
            notes
        )

        transaction_id = create_transaction_with_cursor(
            cursor,
            event_id,
            transaction_type
        )

        transaction_item_id = add_transaction_item_with_cursor(
            cursor,
            transaction_id,
            card_id,
            'IN',
            quantity,
            None,
            location_id,
            foil,
            card_condition,
            price_per_card,
            currency
        )

        collection_result = add_to_collection_with_cursor(
            cursor,
            card_id,
            location_id,
            quantity,
            foil,
            card_condition
        )

        if collection_result is False:
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


def remove_cards_with_transaction(
    event_date,
    transaction_type,
    person_place,
    notes,
    collection_id,
    quantity,
    price_per_card,
    currency
):
    allowed_out_types = [
        "Sale",
        "Trade",
        "Gift",
        "Other"
    ]

    if transaction_type not in allowed_out_types:
        return False

    if quantity < 1:
        return False

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
            (collection_id,)
        )

        collection_entry = cursor.fetchone()

        if collection_entry is None:
            return False

        if quantity > collection_entry["Quantity"]:
            return False

        event_id = create_event_with_cursor(
            cursor,
            event_date,
            "Remove",
            person_place,
            notes
        )

        transaction_id = create_transaction_with_cursor(
            cursor,
            event_id,
            transaction_type
        )

        transaction_item_id = add_transaction_item_with_cursor(
            cursor,
            transaction_id,
            collection_entry["Card_ID"],
            'OUT',
            quantity,
            collection_entry["Location_ID"],
            None,
            collection_entry["Foil"],
            collection_entry["Card_Condition"],
            price_per_card,
            currency
        )

        collection_result = remove_from_collection_with_cursor(
            cursor,
            collection_id,
            quantity
        )

        if collection_result is False:
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


def move_cards_with_transaction(
    event_date,
    person_place,
    notes,
    collection_id,
    to_location_id,
    quantity
):
    if quantity < 1:
        return False

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
            (collection_id,)
        )

        collection_entry = cursor.fetchone()

        if collection_entry is None:
            return False

        if to_location_id == collection_entry["Location_ID"]:
            return False

        if quantity > collection_entry["Quantity"]:
            return False

        event_id = create_event_with_cursor(
            cursor,
            event_date,
            "Move",
            person_place,
            notes
        )

        transaction_id = create_transaction_with_cursor(
            cursor,
            event_id,
            "Internal Move"
        )

        transaction_item_id = add_transaction_item_with_cursor(
            cursor,
            transaction_id,
            collection_entry["Card_ID"],
            'MOVE',
            quantity,
            collection_entry["Location_ID"],
            to_location_id,
            collection_entry["Foil"],
            collection_entry["Card_Condition"],
            None,
            None
        )

        remove_result = remove_from_collection_with_cursor(
            cursor,
            collection_id,
            quantity
        )

        if remove_result is False:
            connection.rollback()
            return False

        add_result = add_to_collection_with_cursor(
            cursor,
            collection_entry["Card_ID"],
            to_location_id,
            quantity,
            collection_entry["Foil"],
            collection_entry["Card_Condition"]
        )

        if add_result is False:
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


def increase_collection_with_transaction(
    event_date,
    transaction_type,
    person_place,
    notes,
    collection_id,
    price_per_card,
    currency
):
    allowed_in_types = [
        "Purchase",
        "Trade",
        "Gift",
        "Other"
    ]

    if transaction_type not in allowed_in_types:
        return False

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
            (collection_id,)
        )

        collection_entry = cursor.fetchone()

        if collection_entry is None:
            return False

        event_id = create_event_with_cursor(
            cursor,
            event_date,
            "Add",
            person_place,
            notes
        )

        transaction_id = create_transaction_with_cursor(
            cursor,
            event_id,
            transaction_type
        )

        transaction_item_id = add_transaction_item_with_cursor(
            cursor,
            transaction_id,
            collection_entry["Card_ID"],
            'IN',
            1,
            None,
            collection_entry["Location_ID"],
            collection_entry["Foil"],
            collection_entry["Card_Condition"],
            price_per_card,
            currency
        )

        collection_result = add_to_collection_with_cursor(
            cursor,
            collection_entry["Card_ID"],
            collection_entry["Location_ID"],
            1,
            collection_entry["Foil"],
            collection_entry["Card_Condition"]
        )

        if collection_result is False:
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


def decrease_collection_with_transaction(
    event_date,
    transaction_type,
    person_place,
    notes,
    collection_id,
    price_per_card,
    currency
):
    allowed_out_types = [
        "Sale",
        "Trade",
        "Gift",
        "Other"
    ]

    if transaction_type not in allowed_out_types:
        return False

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
            (collection_id,)
        )

        collection_entry = cursor.fetchone()

        if collection_entry is None:
            return False

        if collection_entry["Quantity"] < 1:
            return False

        event_id = create_event_with_cursor(
            cursor,
            event_date,
            "Remove",
            person_place,
            notes
        )

        transaction_id = create_transaction_with_cursor(
            cursor,
            event_id,
            transaction_type
        )

        transaction_item_id = add_transaction_item_with_cursor(
            cursor,
            transaction_id,
            collection_entry["Card_ID"],
            'OUT',
            1,
            collection_entry["Location_ID"],
            None,
            collection_entry["Foil"],
            collection_entry["Card_Condition"],
            price_per_card,
            currency
        )

        collection_result = remove_from_collection_with_cursor(
            cursor,
            collection_id,
            1
        )

        if collection_result is False:
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


def remove_all_collection_with_transaction(
    event_date,
    transaction_type,
    person_place,
    notes,
    collection_id,
    price_per_card,
    currency
):
    allowed_out_types = [
        "Sale",
        "Trade",
        "Gift",
        "Other"
    ]

    if transaction_type not in allowed_out_types:
        return False

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
            (collection_id,)
        )

        collection_entry = cursor.fetchone()

        if collection_entry is None:
            return False

        event_id = create_event_with_cursor(
            cursor,
            event_date,
            "Remove",
            person_place,
            notes
        )

        transaction_id = create_transaction_with_cursor(
            cursor,
            event_id,
            transaction_type
        )

        transaction_item_id = add_transaction_item_with_cursor(
            cursor,
            transaction_id,
            collection_entry["Card_ID"],
            'OUT',
            collection_entry["Quantity"],
            collection_entry["Location_ID"],
            None,
            collection_entry["Foil"],
            collection_entry["Card_Condition"],
            price_per_card,
            currency
        )

        collection_result = remove_from_collection_with_cursor(
            cursor,
            collection_id,
            collection_entry["Quantity"]
        )

        if collection_result is False:
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


def edit_collection_with_transaction(
    collection_id,
    new_location_id,
    new_quantity,
    new_foil,
    new_card_condition,
    is_correction,
    event_date=None,
    transaction_type=None,
    person_place=None,
    notes=None,
    price_per_card=None,
    currency=None
):
    if new_quantity < 1:
        return False

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
            (collection_id,)
        )

        collection_entry = cursor.fetchone()

        if collection_entry is None:
            return False

        if is_correction:
            result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                new_location_id,
                new_quantity,
                new_foil,
                new_card_condition
            )

            if result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        location_changed = collection_entry["Location_ID"] != new_location_id
        quantity_changed = collection_entry["Quantity"] != new_quantity
        variant_changed = (
                collection_entry["Foil"] != new_foil
                or collection_entry["Card_Condition"] != new_card_condition
        )

        if not location_changed and not quantity_changed and not variant_changed:
            return False

        quantity_difference = new_quantity - collection_entry["Quantity"]

        if quantity_difference > 0:
            allowed_in_types = [
                "Purchase",
                "Trade",
                "Gift",
                "Other"
            ]

            if transaction_type not in allowed_in_types:
                return False

        elif quantity_difference < 0:
            allowed_out_types = [
                "Sale",
                "Trade",
                "Gift",
                "Other"
            ]

            if transaction_type not in allowed_out_types:
                return False

        event_id = create_event_with_cursor(
            cursor,
            event_date,
            "Edit",
            person_place,
            notes
        )

        if quantity_changed and not location_changed and not variant_changed and quantity_difference > 0:
            transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                transaction_type
            )

            add_transaction_item_with_cursor(
                cursor,
                transaction_id,
                collection_entry["Card_ID"],
                'IN',
                quantity_difference,
                None,
                collection_entry["Location_ID"],
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                price_per_card,
                currency
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                new_location_id,
                new_quantity,
                new_foil,
                new_card_condition
            )

            if update_result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        elif quantity_changed and not location_changed and not variant_changed and quantity_difference < 0:
            transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                transaction_type
            )

            add_transaction_item_with_cursor(
                cursor,
                transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                abs(quantity_difference),
                collection_entry["Location_ID"],
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                price_per_card,
                currency
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                new_location_id,
                new_quantity,
                new_foil,
                new_card_condition
            )

            if update_result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        elif location_changed and not quantity_changed and not variant_changed:
            transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Internal Move"
            )

            add_transaction_item_with_cursor(
                cursor,
                transaction_id,
                collection_entry["Card_ID"],
                'MOVE',
                collection_entry["Quantity"],
                collection_entry["Location_ID"],
                new_location_id,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                new_location_id,
                collection_entry["Quantity"],
                collection_entry["Foil"],
                collection_entry["Card_Condition"]
            )

            if update_result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        elif not location_changed and not quantity_changed and variant_changed:
            transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Other"
            )

            add_transaction_item_with_cursor(
                cursor,
                transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                collection_entry["Quantity"],
                collection_entry["Location_ID"],
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            add_transaction_item_with_cursor(
                cursor,
                transaction_id,
                collection_entry["Card_ID"],
                'IN',
                collection_entry["Quantity"],
                None,
                collection_entry["Location_ID"],
                new_foil,
                new_card_condition,
                None,
                None
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                collection_entry["Location_ID"],
                collection_entry["Quantity"],
                new_foil,
                new_card_condition
            )

            if update_result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        elif location_changed and quantity_changed and not variant_changed and quantity_difference > 0:
            internal_move_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Internal Move"
            )

            add_transaction_item_with_cursor(
                cursor,
                internal_move_transaction_id,
                collection_entry["Card_ID"],
                'MOVE',
                collection_entry["Quantity"],
                collection_entry["Location_ID"],
                new_location_id,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            in_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                transaction_type
            )

            add_transaction_item_with_cursor(
                cursor,
                in_transaction_id,
                collection_entry["Card_ID"],
                'IN',
                quantity_difference,
                None,
                new_location_id,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                price_per_card,
                currency
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                new_location_id,
                new_quantity,
                collection_entry["Foil"],
                collection_entry["Card_Condition"]
            )

            if update_result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        elif location_changed and quantity_changed and not variant_changed and quantity_difference < 0:
            internal_move_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Internal Move"
            )

            add_transaction_item_with_cursor(
                cursor,
                internal_move_transaction_id,
                collection_entry["Card_ID"],
                'MOVE',
                new_quantity,
                collection_entry["Location_ID"],
                new_location_id,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            out_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                transaction_type
            )

            add_transaction_item_with_cursor(
                cursor,
                out_transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                abs(quantity_difference),
                collection_entry["Location_ID"],
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                price_per_card,
                currency
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                new_location_id,
                new_quantity,
                collection_entry["Foil"],
                collection_entry["Card_Condition"]
            )

            if update_result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        elif not location_changed and quantity_changed and variant_changed and quantity_difference > 0:
            variant_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Other"
            )

            add_transaction_item_with_cursor(
                cursor,
                variant_transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                collection_entry["Quantity"],
                collection_entry["Location_ID"],
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            add_transaction_item_with_cursor(
                cursor,
                variant_transaction_id,
                collection_entry["Card_ID"],
                'IN',
                collection_entry["Quantity"],
                None,
                collection_entry["Location_ID"],
                new_foil,
                new_card_condition,
                None,
                None
            )

            in_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                transaction_type
            )

            add_transaction_item_with_cursor(
                cursor,
                in_transaction_id,
                collection_entry["Card_ID"],
                'IN',
                quantity_difference,
                None,
                collection_entry["Location_ID"],
                new_foil,
                new_card_condition,
                price_per_card,
                currency
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                collection_entry["Location_ID"],
                new_quantity,
                new_foil,
                new_card_condition
            )

            if update_result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        elif not location_changed and quantity_changed and variant_changed and quantity_difference < 0:
            out_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                transaction_type
            )

            add_transaction_item_with_cursor(
                cursor,
                out_transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                abs(quantity_difference),
                collection_entry["Location_ID"],
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                price_per_card,
                currency
            )

            variant_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Other"
            )

            add_transaction_item_with_cursor(
                cursor,
                variant_transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                new_quantity,
                collection_entry["Location_ID"],
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            add_transaction_item_with_cursor(
                cursor,
                variant_transaction_id,
                collection_entry["Card_ID"],
                'IN',
                new_quantity,
                None,
                collection_entry["Location_ID"],
                new_foil,
                new_card_condition,
                None,
                None
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                collection_entry["Location_ID"],
                new_quantity,
                new_foil,
                new_card_condition
            )

            if update_result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        elif location_changed and not quantity_changed and variant_changed:
            internal_move_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Internal Move"
            )

            add_transaction_item_with_cursor(
                cursor,
                internal_move_transaction_id,
                collection_entry["Card_ID"],
                'MOVE',
                collection_entry["Quantity"],
                collection_entry["Location_ID"],
                new_location_id,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            variant_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Other"
            )

            add_transaction_item_with_cursor(
                cursor,
                variant_transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                collection_entry["Quantity"],
                new_location_id,
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            add_transaction_item_with_cursor(
                cursor,
                variant_transaction_id,
                collection_entry["Card_ID"],
                'IN',
                collection_entry["Quantity"],
                None,
                new_location_id,
                new_foil,
                new_card_condition,
                None,
                None
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                new_location_id,
                collection_entry["Quantity"],
                new_foil,
                new_card_condition
            )

            if update_result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        elif location_changed and quantity_changed and variant_changed and quantity_difference > 0:
            internal_move_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Internal Move"
            )

            add_transaction_item_with_cursor(
                cursor,
                internal_move_transaction_id,
                collection_entry["Card_ID"],
                'MOVE',
                collection_entry["Quantity"],
                collection_entry["Location_ID"],
                new_location_id,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            variant_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Other"
            )

            add_transaction_item_with_cursor(
                cursor,
                variant_transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                collection_entry["Quantity"],
                new_location_id,
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            add_transaction_item_with_cursor(
                cursor,
                variant_transaction_id,
                collection_entry["Card_ID"],
                'IN',
                collection_entry["Quantity"],
                None,
                new_location_id,
                new_foil,
                new_card_condition,
                None,
                None
            )

            in_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                transaction_type
            )

            add_transaction_item_with_cursor(
                cursor,
                in_transaction_id,
                collection_entry["Card_ID"],
                'IN',
                quantity_difference,
                None,
                new_location_id,
                new_foil,
                new_card_condition,
                price_per_card,
                currency
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                new_location_id,
                new_quantity,
                new_foil,
                new_card_condition
            )

            if update_result is False:
                connection.rollback()
                return False

            connection.commit()
            return True

        elif location_changed and quantity_changed and variant_changed and quantity_difference < 0:
            out_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                transaction_type
            )

            add_transaction_item_with_cursor(
                cursor,
                out_transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                abs(quantity_difference),
                collection_entry["Location_ID"],
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                price_per_card,
                currency
            )

            internal_move_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Internal Move"
            )

            add_transaction_item_with_cursor(
                cursor,
                internal_move_transaction_id,
                collection_entry["Card_ID"],
                'MOVE',
                new_quantity,
                collection_entry["Location_ID"],
                new_location_id,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            variant_transaction_id = create_transaction_with_cursor(
                cursor,
                event_id,
                "Other"
            )

            add_transaction_item_with_cursor(
                cursor,
                variant_transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                new_quantity,
                new_location_id,
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                None,
                None
            )

            add_transaction_item_with_cursor(
                cursor,
                variant_transaction_id,
                collection_entry["Card_ID"],
                'IN',
                new_quantity,
                None,
                new_location_id,
                new_foil,
                new_card_condition,
                None,
                None
            )

            update_result = update_collection_entry_with_cursor(
                cursor,
                collection_id,
                new_location_id,
                new_quantity,
                new_foil,
                new_card_condition
            )

            if update_result is False:
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


def trade_cards_with_transaction(
        event_date,
        person_place,
        notes,
        outgoing_cards,
        incoming_cards
):
    if not outgoing_cards or not incoming_cards:
        return False

    for outgoing_card in outgoing_cards:
        if outgoing_card["quantity"] < 1:
            return False

        if outgoing_card["price_per_card"] is not None and outgoing_card["currency"] is None:
            return False

        if outgoing_card["price_per_card"] is None and outgoing_card["currency"] is not None:
            return False

    allowed_conditions = [
        "Near Mint",
        "Lightly Played",
        "Moderately Played",
        "Heavily Played",
        "Damaged"
    ]

    for incoming_card in incoming_cards:
        if incoming_card["quantity"] < 1:
            return False

        if incoming_card["price_per_card"] is not None and incoming_card["currency"] is None:
            return False

        if incoming_card["price_per_card"] is None and incoming_card["currency"] is not None:
            return False

        if incoming_card["card_condition"] not in allowed_conditions:
            return False

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        outgoing_collection_entries = []

        for outgoing_card in outgoing_cards:
            cursor.execute(""" SELECT * 
                               FROM Collection
                               WHERE Collection_ID = %s 
                                 AND Is_Deleted = 0
                """,
                    (outgoing_card["collection_id"],)
            )

            collection_entry = cursor.fetchone()

            if collection_entry is None:
               return False

            if outgoing_card["quantity"] > collection_entry["Quantity"]:
                return False

            outgoing_collection_entries.append(collection_entry)

        event_id = create_event_with_cursor(
            cursor,
            event_date,
            "Trade",
            person_place,
            notes
        )

        transaction_id = create_transaction_with_cursor(
            cursor,
            event_id,
            "Trade"
        )

        for outgoing_card, collection_entry in zip(
                outgoing_cards,
                outgoing_collection_entries
        ):
            add_transaction_item_with_cursor(
                cursor,
                transaction_id,
                collection_entry["Card_ID"],
                'OUT',
                outgoing_card["quantity"],
                collection_entry["Location_ID"],
                None,
                collection_entry["Foil"],
                collection_entry["Card_Condition"],
                outgoing_card["price_per_card"],
                outgoing_card["currency"]
            )

            result = remove_from_collection_with_cursor(
                cursor,
                collection_entry["Collection_ID"],
                outgoing_card["quantity"]
            )

            if result is False:
                connection.rollback()
                return False

        for incoming_card in incoming_cards:
            add_transaction_item_with_cursor(
                cursor,
                transaction_id,
                incoming_card["card_id"],
                'IN',
                incoming_card["quantity"],
                None,
                incoming_card["location_id"],
                incoming_card["foil"],
                incoming_card["card_condition"],
                incoming_card["price_per_card"],
                incoming_card["currency"]
            )

            result = add_to_collection_with_cursor(
                cursor,
                incoming_card["card_id"],
                incoming_card["location_id"],
                incoming_card["quantity"],
                incoming_card["foil"],
                incoming_card["card_condition"]
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