import sqlite3


class Record:
    def __init__(self):
        self.connection = sqlite3.connect('src/game_records.db')
        self.cursor = self.connection.cursor()

    def get_best_score(self):
        try:
            self.connection = sqlite3.connect('src/game_records.db')
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
            SELECT score FROM score_records
            """)
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)
        records = []
        sql_records = self.cursor.fetchall()
        self.connection.close()
        for list_el in sql_records:
            for tuple_el in list_el:
                records.append(tuple_el)
        if not records:
            return 0
        return max(records)

    def insert_record(self, date, score):
        try:
            self.connection = sqlite3.connect('src/game_records.db')
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
            INSERT INTO score_records VALUES 
            ('{}', {})""".format(date, score)
                                )
            self.connection.commit()
            self.connection.close()
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)


'''
connection = sqlite3.connect('src/game_records.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE score_records (
    date TEXT PRIMARY KEY,
    score INTEGER
)
""")

connection.commit()

connection.close()
'''