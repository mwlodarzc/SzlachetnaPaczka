import itertools
from db import Database

class MockData:
    __tables = [
        "person",
        "user_data",
        "help_group",
        "caretaker",
        "donor",
        "donations",
        "needs",
        "product",
    ]

    @staticmethod
    def load_table(table_name: str, db: Database) -> None:
        # print(table_name)
        for line in open(f"./mock_data/{table_name}.csv", "r").readlines()[1:]:
            getattr(db, f"add_{table_name}")(*line.rstrip().split(","))

    @staticmethod
    def load(db: Database) -> None:
        for table in __class__.__tables:
            __class__.load_table(table, db)
        # for table in __class__.__tables:
        # __class__.load_table(table, db)
        __class__.connect_person(db)
        __class__.connect_user_data(db)
        __class__.connect_needs_products(db)
        __class__.connect_help_group(db)
        __class__.connect_donor(db)
        __class__.connect_donation(db)
        # for e in db.select_all("person"):
        # print(e, end="\n")

    @staticmethod
    def show(db: Database) -> None:
        # file = open("mock_data/mock_data.txt", "w")
        for table in __class__.__tables:
            print(table)
            # file.write(f"{table}\n")
            # for entry in db.select_all(table):
            # file.write(f"{str(entry)}\n")
            print(db.select_all(table))

    @staticmethod
    def connect_person(db: Database) -> None:
        # print("BEGIN CARETAKER")
        for i in range(1, 21):
            db.update("person", i, person_caretaker_ref_id=i)
        #     print(i)
        # print("END CARETAKER")
        # print("BEGIN DONOR")
        for i in range(21, 61):
            db.update("person", i, person_donor_ref_id=i - 20)
        #     print(i)
        # print("END DONOR")
        # print("BEGIN HELP_GROUP")
        for i in range(61, 161):
            db.update("person", i, person_help_group_ref_id=i % 20 + 1)
        #     print(i % 20 + 1)
        # print("END HELP_GROUP_1")
        # print("BEGIN HELP_GROUP_2")
        for i in range(161, 201):
            db.update("person", i, person_help_group_ref_id=21 + i % 5)
        #     print(21 + i % 5)
        # print("END HELP_GROUP_2")

    @staticmethod
    def connect_user_data(db: Database) -> None:
        for i in range(1, 61):
            db.update("person", i, person_user_data_ref_id=i)
            # print(db.select_id("person", i))

    @staticmethod
    def connect_needs_products(db: Database) -> None:
        for i, j in itertools.product(range(1, 26), range(1, 21)):
            db.update(
                "needs",
                (i * 20) + j - 20,
                needs_help_group_ref_id=i,
                needs_products_ref_id=j,
            )
        # for i in range(1, 501):
        #     print(db.select_id("needs", i))

    @staticmethod
    def connect_help_group(db: Database) -> None:
        for i in range(1, 21):
            db.update("help_group", i, help_group_caretaker_ref_id=i)
        for i in range(1, 6):
            db.update("help_group", i + 20, help_group_caretaker_ref_id=i)

    @staticmethod
    def connect_donor(db: Database) -> None:
        for i in range(1, 26):
            db.update("donor", i, donor_help_group_ref_id=i)

    @staticmethod
    def connect_donation(db: Database) -> None:
        for i in range(1, 81):
            db.update(
                "donations",
                i,
                donations_donor_ref_id=i % 40 + 1,
                donations_help_group_ref_id=i % 25 + 1,
            )
            # print(db.select_id("donations", i))