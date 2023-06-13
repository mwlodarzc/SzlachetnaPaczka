import itertools
from db import Database

class MockData:
    __tables = [
        "person",
        "user_data",
        "help_group",
        "donation",
        "needs",
        "product",
    ]

    @staticmethod
    def load_table(table_name: str, db: Database) -> None:
        for line in open(f"./mock_data/{table_name}.csv", "r").readlines()[1:]:
            # print(table_name, line.rstrip().split(","))
            getattr(db, f"add_{table_name}")(*line.rstrip().split(","))

    @staticmethod
    def load(db: Database) -> None:
        for table in __class__.__tables:
            __class__.load_table(table, db)
        for _ in range(1000):
            db.add_caretaker()
        for _ in range(1000):
            db.add_donor()

        __class__.connect_person(db)
        __class__.connect_needs(db)
        __class__.connect_help_group(db)
        __class__.connect_donation(db)


    @staticmethod
    def show(db: Database) -> None:
        # file = open("mock_data/mock_data.txt", "w")
        for table in __class__.__tables:
            print(table)
        #     # file.write(f"{table}\n")
        #     # for entry in db.select_all(table):
        #     # file.write(f"{str(entry)}\n")
            for row in db.select_all(table):
                print(row)

    @staticmethod
    def connect_person(db: Database) -> None:
        # print("BEGIN CARETAKER")
        for i in range(1, 101):
            db.update("person", i, person_caretaker_ref_id=i)
        #     print(i)
        # print("END CARETAKER")
        # print("BEGIN DONOR")
        for i in range(101, 301):
            db.update("person", i, person_donor_ref_id=i % 200 + 1)
        #     print(i)
        # print("END DONOR")
        # print("BEGIN HELP_GROUP")
        for i in range(301, 1001):
            db.update("person", i, person_help_group_ref_id=i % 140 + 1)
        #     print(i % 20 + 1)
        # print("END HELP_GROUP")
        for i in range(1, 301):
            db.update("person", i, person_user_data_ref_id=i)

    # @staticmethod
    # def connect_needs_products(db: Database) -> None:
    #     for i, j in itertools.product(range(1, 26), range(1, 21)):
    #         db.update(
    #             "needs",
    #             (i * 20) + j - 20,
    #             needs_help_group_ref_id=i,
    #             needs_products_ref_id=j,
    #         )
    #     # for i in range(1, 501):
    #     #     print(db.select_id("needs", i))

    @staticmethod
    def connect_help_group(db: Database) -> None:
        for i in range(1, 50):
            db.update("help_group", i, help_group_caretaker_ref_id=i)


    @staticmethod
    def connect_needs(db: Database) -> None:
        for i in range(1, 1001):
            db.update(
                "needs",
                i,
                needs_help_group_ref_id=i % 140 +1,
                needs_products_ref_id=i
            )


    @staticmethod
    def connect_donation(db: Database) -> None:
        for i in range(1, 1001):
            db.update(
                "donation",
                i,
                donation_donor_ref_id=i % 200 + 1,
                donation_help_group_ref_id=i % 140 + 1,
            )
            # print(db.select_id("donations", i))