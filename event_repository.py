import mysql.connector
from database import get_connection


def create_event_with_cursor(
    cursor,
    event_date,
    event_type,
    person_place,
    notes
):
    cursor.execute("""INSERT INTO Collection_Event (Event_Date, Event_Type, Person_Place, Notes)
                      VALUES (%s, %s, %s, %s)
                   """,
                   (event_date, event_type, person_place, notes)
                   )

    event_id = cursor.lastrowid

    return event_id


def create_event(event_date, event_type, person_place, notes):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        event_id = create_event_with_cursor(
            cursor,
            event_date,
            event_type,
            person_place,
            notes
        )

        connection.commit()
        return event_id

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


def get_all_events():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """ SELECT * FROM Collection_Event
                ORDER BY Event_Date DESC,
                         Created_At DESC,
                         Event_ID DESC
            """
        )

        all_events = cursor.fetchall()
        return all_events

    except mysql.connector.Error as error:
        print(error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()