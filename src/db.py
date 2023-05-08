import os
import psycopg2
from config import config


class Database:
    LEVEL = ("low", "mid", "mid")

    def __init__(self):
        params = config()
        # print('Connecting to the postgreSQL database ...')
        # print(params)

        self.connector = psycopg2.connect(**params)
        # cursor = self.connector.cursor()
        #     # print('PostgreSQL database version: ')
        #     # cursor.execute("SELECT version()")
        #     # db_version = cursor.fetchone()
        #     # print(db_version)
        #     # cursor.close()
        cursor = self.connector.cursor()
        cursor.execute(open("src/drop.sql", "r").read())
        cursor.execute(open("src/init.sql", "r").read())
        cursor.close()
        self.connector.commit()

    def __del__(self):
        self.connector.close()

    def register_account(
        self,
        user_info: tuple,
    ):
        ...
        # add_user(self, user_info)

    def select_id(self, table: str, id: int) -> tuple:
        cursor = self.connector.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {table}_id={id}")
        tmp = cursor.fetchone()
        cursor.close()
        self.connector.commit()
        return tmp

    def update(self, table: str, id: int, **kwargs):
        for kw in kwargs:
            cursor = self.connector.cursor()
            cursor.execute(
                f"UPDATE {table} SET {kw} = {kwargs[kw]} WHERE {table}_id = {id};"
            )
            cursor.close()
            self.connector.commit()

    def delete(self, table: str, id: int):
        cursor = self.connector.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE {table}_id = {id};")
        cursor.close()
        self.connector.commit()

    def add_user(
        self,
        email_address: str,
        phone_number: str,
        password_hash: str,
        modification_date: str,
        join_date: str,
    ):
        with self.connector.cursor() as cur:
            cur.execute(
                "INSERT INTO user_data (email_address,phone_number,password_hash,modification_date,join_date) VALUES(%s,%s,%s,%s,%s) RETURNING user_data_id;",
                (
                    email_address,
                    phone_number,
                    password_hash,
                    modification_date,
                    join_date,
                ),
            )
            tmp = cur.fetchone()[0]
            self.connector.commit()
            cur.close()
            return tmp

    def add_caretaker(
        self,
        donation_place: str,
        car_owner: str,
        active_hours_start: str,
        active_hours_end: str,
    ):
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO caretaker (donation_place,car_owner, active_hours_start,active_hours) VALUES (%s,%s,%s,%s) RETURNING caretaker_id;",
            (donation_place, car_owner, active_hours_start, active_hours_end),
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_help_group(self, poverty_level: str):
        # test
        assert poverty_level not in self.LEVEL
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO help_group VALUES (%s) RETURNING help_group_id", poverty_level
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_product(self, kind: str):
        cur = self.connector.cursor()
        self.cursor.execute(
            "INSERT INTO product VALUES (%s) RETURNING product_id;", kind
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_needs(self, count: int):
        cur = self.connector.cursor()
        cur.execute("INSERT INTO needs (count) VALUES (%s) RETURNING needs_id;", count)
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_donor(self, pack_count: int, donations_sum: int, points: int):
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO donor (pack_count, donations_sum, points) VALUES (%s,%s,%s) RETURNING donor_id;",
            (pack_count, donations_sum, points),
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_donations(self, date: str, note: str):
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO donations (date, note) VALUES (%s,%s) RETURNING donations_id;",
            (date, note),
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_person(
        self, pesel: str, forename: str, surname: str, address: str, birth: str
    ):
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO person (pesel, forename, surname, address, birth) VALUES (%s,%s,%s,%s,%s) RETURNING person_id;",
            (pesel, forename, surname, address, birth),
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp
