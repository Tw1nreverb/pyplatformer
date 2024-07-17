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


def check_coins(username):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
        )
        with connection.cursor() as cursor:
            cursor.execute(
                """Select "Game"."game_id","Game"."coin" from public."User" Join public."Game" on "User"."User_id"="Game"."user_id" Where "User"."username" 
                = %s""", (username, ))
            result = cursor.fetchall()
            if result:
                return result
            else:
                return -1
    except Exception as ex:
        print("[INFO] Error while working with PostgreSql", ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSql connection closed")


def add_stats(username, coins, game_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
        )
        user_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                """Select "User_id" from "User" WHERE "username" = %s""",
                (username, ))
            user_id = cursor.fetchone()
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO "Game" VALUES (%s,%s,%s)""",
                           (user_id, coins, game_id))
            connection.commit()
    except Exception as ex:
        print("[INFO] Error while working with PostgreSql", ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSql connection closed")
