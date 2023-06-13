import os
import psycopg2
from config import config
from psycopg2.sql import SQL

class Database:
    LEVEL = ("low", "mid", "mid")

    def __init__(self):
        params = config()
        print('Connecting to the postgreSQL database ...')

        self.connector = psycopg2.connect(**params)
        cursor = self.connector.cursor()
        cursor.execute(open("src/drop.sql", "r").read())
        cursor.execute("SET datestyle TO 'ISO, DMY';")
        cursor.execute(open("src/init.sql", "r").read())
        cursor.close()
        self.connector.commit()

    def __del__(self):
        self.connector.close()

    def is_empty(self, table: str) -> bool:
        cursor = self.connector.cursor()
        isEmpty = True
        try:
            cursor.execute(f"SELECT * FROM {table}")
            tmp = cursor.fetchone()
            isEmpty = not tmp
        except Exception:
            isEmpty = True

        cursor.close()
        self.connector.commit()
        return isEmpty

    def select_id(self, table: str, id: int) -> tuple:
        cursor = self.connector.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {table}_id={id}")
        tmp = cursor.fetchone()
        cursor.close()
        self.connector.commit()
        return tmp
    
    def select_all(self, table: str) -> tuple:
        cursor = self.connector.cursor()
        cursor.execute(f"SELECT * FROM {table};")
        tmp = cursor.fetchall()
        cursor.close()
        self.connector.commit()
        return tmp
    
    def select_ref_id(self, table: str, refTable: str, refId: int) -> tuple:
        cursor = self.connector.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {table}_{refTable}_ref_id={refId}")
        tmp = cursor.fetchone()
        cursor.close()
        self.connector.commit()
        return tmp
    
    def select_email_passwd(self, email_address: str, password_hash: str) -> tuple:
        cursor = self.connector.cursor()
        cursor.execute(f"SELECT * FROM user_data WHERE email_address='{email_address}' AND password_hash='{password_hash}'")
        tmp = cursor.fetchone()
        cursor.close()
        self.connector.commit()
        return tmp
    
    def update(self, table: str, id: int, **kwargs):
        cursor = self.connector.cursor()
        for kw in kwargs:
            cursor.execute(
                f"UPDATE {table} SET {kw} = {kwargs[kw]} WHERE {table}_id = {id};"
            )
        cursor.close()
        self.connector.commit()
    
    def update_selected(self, table: str, id: int, record: str, content: str):
        cursor = self.connector.cursor()
        cursor.execute(f"UPDATE {table} SET {record} = '{content}' WHERE {table}_id = {id};")
        cursor.close()
        self.connector.commit()

    def delete(self, table: str, id: int):
        cursor = self.connector.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE {table}_id = {id};")
        cursor.close()
        self.connector.commit()

    def add_user_data(
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
        verified: bool = False,
        car_owner: bool = False,
    ):
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO caretaker (verified, car_owner) VALUES (%s,%s) RETURNING caretaker_id;",
            [verified, car_owner],
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp
    
    # def add_caretaker_empty(
    #     self,
    # ):
    #     verified = car_owner = False
    #     cur = self.connector.cursor()
    #     cur.execute(
    #         "INSERT INTO caretaker (verified, car_owner) VALUES (%s,%s) RETURNING caretaker_id;",
    #         [verified, car_owner],
    #     )
    #     tmp = cur.fetchone()[0]
    #     self.connector.commit()
    #     cur.close()
    #     return tmp

    def add_help_group(self, monetary_goal: str, finish_date:str, poverty_level: str):
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO help_group (monetary_goal, finish_date, poverty_level) VALUES (%s,%s,%s) RETURNING help_group_id",
            [float(monetary_goal),finish_date,poverty_level],
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_product(self, kind: str,  price: str):
        cur = self.connector.cursor()
        cur.execute(
            SQL("INSERT INTO product (kind,price) VALUES (%s,%s) RETURNING product_id;"), [kind,float(price)]
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_needs(self, count:int):
        cur = self.connector.cursor()
        cur.execute("INSERT INTO needs (count) VALUES (%s) RETURNING needs_id;", [count])
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_donor(self, donations_sum: int = 0, points: int = 0):
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO donor (donations_sum, points) VALUES (%s,%s) RETURNING donor_id;",
            [donations_sum, points],
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_donation(self, date: str, amount: str, note: str):
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO donation (date,amount, note) VALUES (%s,%s,%s) RETURNING donation_id;",
            [date, float(amount), note],
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
            [pesel, forename, surname, address, birth],
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp

    def add_person_caretaker(
        self, forename: str, surname: str, person_caretaker_ref_id: int, person_user_data_ref_id: int
    ):
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO person (forename, surname, person_caretaker_ref_id, person_user_data_ref_id) VALUES (%s,%s,%s,%s) RETURNING person_id;",
            [forename, surname, person_caretaker_ref_id, person_user_data_ref_id],
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp
    
    def add_person_donor(
        self, forename: str, surname: str, person_donor_ref_id: int, person_user_data_ref_id: int
    ):
        cur = self.connector.cursor()
        cur.execute(
            "INSERT INTO person (forename, surname, person_donor_ref_id, person_user_data_ref_id) VALUES (%s,%s,%s,%s) RETURNING person_id;",
            [forename, surname, person_donor_ref_id, person_user_data_ref_id],
        )
        tmp = cur.fetchone()[0]
        self.connector.commit()
        cur.close()
        return tmp