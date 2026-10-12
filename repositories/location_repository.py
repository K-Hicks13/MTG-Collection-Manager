import mysql.connector
from database import get_connection


def get_all_locations():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Location")

        locations = cursor.fetchall()

        return locations

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

def add_location(location_name, location_description, location_type):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO Location (Location_Name, Location_Description, Location_Type)
            VALUES (%s, %s, %s)
            """,
            (location_name, location_description, location_type)
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

def get_location_by_id(location_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM Location WHERE Location_ID = %s",
            (location_id,)
        )

        location = cursor.fetchone()

        return location

    except mysql.connector.Error as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

def update_location(location_id, location_name, location_description, location_type):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE Location SET Location_Name = %s, Location_Description = %s, Location_Type = %s WHERE Location_ID = %s",
            (location_name, location_description, location_type, location_id)
        )

        rows_affected = cursor.rowcount
        connection.commit()

        if rows_affected > 0:
            return True
        else:
            return False

    except mysql.connector.Error as error:
        print(error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()