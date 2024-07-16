import psycopg2
from config import host, user, password, db_name
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
            print("[INFO] Data was succefully inserted")
        connection.commit()
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
                    print("Login succes")
                else:
                    print("login not succes")
            else:
                print("aboba")
    except Exception as ex:
        print("[INFO] Error while working with PostgreSql", ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSql connection closed")


login_user("Vladislav", "qwerty123")
