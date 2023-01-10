import sqlite3
import os
import termcolor
import frame

class SQL:
    """
        Facilitates interactions with the SQL database.
    """

    TESTS_TABLE_NAME = "tests"
    TESTS_TABLE_STRUCT = """
        id INTEGER,
        name TEXT, 
        execution_date TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)"""

    FRAMES_TABLE_NAME = "frames"
    FRAMES_TABLE_STRUCT = """
        test_id INTEGER,

        frame_date TEXT,
        bench_3 TEXT,
        bench_5 TEXT,
        frame_size TEXT,

        MAC_dest TEXT,
        MAC_src TEXT,
        field_1 TEXT,
        field_2 TEXT,
        field_3 TEXT,
        field_4 TEXT,
        field_5 TEXT,
        field_6 TEXT,
        IP_src TEXT,
        IP_dest TEXT,
        field_9 TEXT,
        field_10 TEXT,
        field_11 TEXT,
        field_14 TEXT,
        field_16 TEXT,
        field_17 TEXT,
        field_18 TEXT,
        field_20 TEXT,
        field_21 TEXT,
        field_23 TEXT,
        field_25 TEXT,
        field_26 TEXT,
        field_27 TEXT,
        field_28 TEXT,
        field_29 TEXT,
        field_30 TEXT,
        field_32 TEXT,
        field_33 TEXT,
        field_34 TEXT,
        field_35 TEXT,

        packet_date TEXT,

        msg_type TEXT"""

    def __init__(self, path_to_db: str="../../db.sql"):
        self.path_to_db = path_to_db
        self.conn = None
        self.cursor = None

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass

    def open_db(self) -> bool:
        """
            Opens the DB and creates required tables.

            Return - true - in case of success,
                   - false - in case of error.
        """
        try:
            #
            # Opens the db.
            #
            self.conn = sqlite3.connect(self.path_to_db)
            self.cursor = self.conn.cursor()

            #
            # Creates the "tests" and "frames" tables.
            #
            if not self.execute_query(f"""CREATE table IF NOT EXISTS {SQL.FRAMES_TABLE_NAME} ({SQL.FRAMES_TABLE_STRUCT})""") or \
                not self.execute_query(f"""CREATE table IF NOT EXISTS {SQL.TESTS_TABLE_NAME} ({SQL.TESTS_TABLE_STRUCT})"""):
                raise

        except:
            print(termcolor.colored("[-]", "red"), f"The SQL DB '{self.path_to_db}' can't be used")
            return False

        return True

    def execute_query(self, query: str) -> bool:
        """
            Facilitates query executions.

            Return - true - in case of success,
                   - false - in case of error.
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()

        except:
            return False

        return True

    def insert_frame(self, frame: frame.Frame) -> bool:
        """
            Creates a test if needed and inserts the frame into the "frames" table.

            Return - true - in case of success,
                   - false - in case of error.
        """

        #
        # Checks if the test exists
        #
        if not self.execute_query(f"""SELECT id FROM {self.TESTS_TABLE_NAME} WHERE name = "{frame.test_name}" AND execution_date = "{frame.test_execution_date}\""""):
            return False

        #
        # If not, creates it
        #
        test_id = self.cursor.fetchone()

        if test_id == None:
            if not self.execute_query(f"""INSERT INTO {self.TESTS_TABLE_NAME} (name, execution_date) VALUES ("{frame.test_name}", "{frame.test_execution_date}")"""):
                print(f"""INSERT INTO {self.TESTS_TABLE_NAME} (name, execution_date) VALUES ("{frame.test_name}", "{frame.test_execution_date}")""")
                return False

            #
            # Gets the new id
            #
            if not self.execute_query(f"""SELECT id FROM {self.TESTS_TABLE_NAME} WHERE name = "{frame.test_name}" AND execution_date = "{frame.test_execution_date}\""""):
                return False
            
            test_id = self.cursor.fetchone()

        if test_id == None:
            return False

        test_id = test_id[0]

        return self.execute_query(f"""INSERT INTO {self.FRAMES_TABLE_NAME} ({SQL.FRAMES_TABLE_STRUCT.replace("TEXT", "").replace("INTEGER", "")}) VALUES (
            "{test_id}",

            "{frame.fields["frame_date"]["value"]}",
            "{frame.fields["bench_3"]["value"]}",
            "{frame.fields["bench_5"]["value"]}",
            "{frame.fields["frame_size"]["value"]}",

            "{frame.fields["MAC_dest"]["value"]}",
            "{frame.fields["MAC_src"]["value"]}",
            "{frame.fields["field_1"]["value"]}",
            "{frame.fields["field_2"]["value"]}",
            "{frame.fields["field_3"]["value"]}",
            "{frame.fields["field_4"]["value"]}",
            "{frame.fields["field_5"]["value"]}",
            "{frame.fields["field_6"]["value"]}",
            "{frame.fields["IP_src"]["value"]}",
            "{frame.fields["IP_dest"]["value"]}",
            "{frame.fields["field_9"]["value"]}",
            "{frame.fields["field_10"]["value"]}",
            "{frame.fields["field_11"]["value"]}",
            "{frame.fields["field_14"]["value"]}",
            "{frame.fields["field_16"]["value"]}",
            "{frame.fields["field_17"]["value"]}",
            "{frame.fields["field_18"]["value"]}",
            "{frame.fields["field_20"]["value"]}",
            "{frame.fields["field_21"]["value"]}",
            "{frame.fields["field_23"]["value"]}",
            "{frame.fields["field_25"]["value"]}",
            "{frame.fields["field_26"]["value"]}",
            "{frame.fields["field_27"]["value"]}",
            "{frame.fields["field_28"]["value"]}",
            "{frame.fields["field_29"]["value"]}",
            "{frame.fields["field_30"]["value"]}",
            "{frame.fields["field_32"]["value"]}",
            "{frame.fields["field_33"]["value"]}",
            "{frame.fields["field_34"]["value"]}",
            "{frame.fields["field_35"]["value"]}",
            "{frame.packet_date}",

            "{frame.message_type}")""")
