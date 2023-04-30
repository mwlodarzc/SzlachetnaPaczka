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

    def add_user(
        self, email_address, phone_number, password_hash, modification_date, join_date
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

    def select_idx(self, table: str, id: int) -> tuple:
        cursor = self.connector.cursor()
        cursor.execute(f"SELECT * FROM {table} user_data_id={id}")
        tmp = cursor.fetchone()
        cursor.close()
        self.connector.commit()
        return tmp

    # def add_caretaker(
    #     self, donation_place, active_hours_start, active_hours_end, car_owner=False
    # ):
    #     self.cursor.execute(
    #         f"INSERT INTO caretaker (donation_place,active_hours_start,active_hours) VALUES ({donation_place},{car_owner},{active_hours_start},{active_hours_end})"
    #     )
    #     self.connector.commit()

    # def add_help_group(self, poverty_level: str):
    #     # test
    #     assert poverty_level not in self.LEVEL
    #     self.cursor.execute(f"INSERT INTO help_group VALUES ({poverty_level}))")
    #     self.connector.commit()

    # def add_product(self, kind):
    #     self.cursor.execute(f"INSERT INTO product VALUES ({kind}))")
    #     self.connector.commit()

    # def add_needs(self, count: int):
    #     self.cursor.execute(f"INSERT INTO needs VALUES ({count}))")
    #     self.connector.commit()

    # def add_donor(self, pack_count: int, donations_sum: int, points: int):
    #     self.cursor.execute(
    #         f"INSERT INTO donor VALUES ({pack_count},{donations_sum},{points}))"
    #     )
    #     self.connector.commit()

    # def add_donations(self, date, note):
    #     self.cursor.execute(f"INSERT INTO donations VALUES ({date},{note}))")
    #     self.connector.commit()

    # def add_person(self, pesel, forename, surname, address, birth):
    #     self.cursor.execute(
    #         f"INSERT INTO person VALUES ({pesel},{forename},{surname},{address},{birth}"
    #     )
    #     self.connector.commit()
