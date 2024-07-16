import psycopg2
from database.config import host, user, password, db_name
from werkzeug.security import generate_password_hash, check_password_hash


def register_user(username, passwor):
    hashed_password = generate_password_hash(passwor)
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
        )
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO public."User"
                ("username","password") VALUES (%s,%s)
            """, (username, hashed_password))
        connection.commit()
        return True
    except Exception as ex:
        print("[INFO] Error while working with PostgreSql", ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSql connection closed")


def login_user(username, passwor):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
        )
        with connection.cursor() as cursor:
            cursor.execute(
                """Select "password" from "User" where "username" = (%s)""",
                (username, ))
            result = cursor.fetchone()
            if result:
                hashed_password = result[0]
                if check_password_hash(hashed_password, passwor):
                    return True
                else:
                    return False
            else:
                return False
    except Exception as ex:
        print("[INFO] Error while working with PostgreSql", ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSql connection closed")


login_user("Vladislav", "qwerty123")
