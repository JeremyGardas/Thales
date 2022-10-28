import sqlite3
import os
import termcolor
import frame

class SQL:
    """
        Facilitates interactions with the SQL database.
    """

    TABLE_NAME = "frames"
    TABLE_STRUCT = """
        test_name TEXT, 
        test_execution_date TEXT,

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

        msg_type TEXT,

        msg TEXT"""

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
            Opens the DB and creates a table.

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
            # Creates a table.
            #
            if not self.execute_query(f"""CREATE table IF NOT EXISTS {SQL.TABLE_NAME} ({SQL.TABLE_STRUCT})"""):
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
            Inserts a frame into the "frames" table.

            Return - true - in case of success,
                   - false - in case of error.
        """

        return self.execute_query(f"""INSERT INTO {self.TABLE_NAME} ({SQL.TABLE_STRUCT.replace("TEXT", "")}) VALUES (
            "{frame.test_name}",
            "{frame.test_execution_date}",

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

            "{frame.message_type}",

            "{bytes(str(frame.msg), "utf-8").hex()}\")""")
