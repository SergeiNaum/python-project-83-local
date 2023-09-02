
import psycopg2

from datetime import datetime
from typing import NamedTuple


from psycopg2.extras import NamedTupleCursor


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor(cursor_factory=NamedTupleCursor)

    def add_url(self, url_name):
        sql = """INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;""", \
              (url_name, datetime.now())
        try:
            self.__cur.execute(sql)
            id = self.__cur.fetchall()
            self.__db.commit()

            if id:
                return id

        except psycopg2.DatabaseError as e:
            print('Ошибка добавления url' + str(e))
        return []

    def create_url_check(self, url, status_code, tags_data):
        try:
            self.__cur.execute(
                """INSERT INTO url_checks\
                    (url_id, status_code, h1, title, description, created_at)\
                    VALUES (%s, %s, %s, %s, %s, %s);""",
                (
                    url.id,
                    status_code,
                    tags_data['h1'],
                    tags_data['title'],
                    tags_data['description'],
                    datetime.now(),
                ),
            )
            self.__db.commit()

        except psycopg2.DatabaseError as e:
            print('Ошибка добавления url в таблицу проверок' + str(e))

    def get_url_by_url_name(self, url_name: str) -> NamedTuple or list:
        try:
            self.__cur.execute('SELECT * FROM urls WHERE name = %s LIMIT 1;', (url_name,), )
            url = self.__cur.fetchone()

            return url

        except psycopg2.DatabaseError as e:
            print('Ошибка извлечения url из БД' + str(e))
        return []

    def get_urls_and_last_checks_data(self):
        sql = """SELECT DISTINCT ON (urls.id) urls.id, urls.name,
                        url_checks.status_code, url_checks.created_at
                    FROM urls
                    LEFT JOIN url_checks ON urls.id = url_checks.url_id
                    ORDER BY urls.id DESC, url_checks.created_at DESC;"""

        try:
            self.__cur.execute(sql)
            data = self.__cur.fetchall()
            return data

        except psycopg2.DatabaseError as e:
            print('Ошибка извлечения url из БД' + str(e))
        return []

    def get_url_by_id(self, url_id):
        try:
            self.__cur.execute(
                """SELECT * FROM urls WHERE id = %s LIMIT 1;""", (url_id,))
            url = self.__cur.fetchone()

            return url

        except psycopg2.DatabaseError as e:
            print('Ошибка извлечения url из БД' + str(e))
        return []

    def get_url_checks_by_url_id(self, url_id):
        try:
            self.__cur.execute(
                """SELECT *
                    FROM url_checks
                    WHERE url_id = %s
                    ORDER BY id DESC;""", (url_id,)
            )
            url_checks = self.__cur.fetchall()
            return url_checks

        except psycopg2.DatabaseError as e:
            print('Ошибка извлечения url из БД' + str(e))
        return []
