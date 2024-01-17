import sqlite3


class Database:
    def __init__(self):
        pass

    def create_table(self, path, table, parameters):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({parameters})")
        connection.commit()

    def delete_value(self, path, table, value1, value2):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM {table} WHERE {value1} = {value2}")

    def get_data(self, path, table, parameters):
            connection = sqlite3.connect(path)
            cursor = connection.cursor()

            if parameters:
                cursor.execute(f"SELECT {parameters} FROM {table}")
            else:
                cursor.execute(f"SELECT * FROM {table}")

            fetchall = cursor.fetchall()
            return fetchall

    def insert_value(self, path, table, *args):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO {table} VALUES {args}")
        connection.commit()

    '''def sort_data(self, path, table):
        data = self.get_data(path, table, None)

        for item in range(0, len(data)):
            if data[item][0] > data[item+1][0]:'''

    def update_value(self, path, table, set1, set2, where1, where2):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute(f"UPDATE {table} SET {set1} = {set2} WHERE {where1} = '{where2}'")
        connection.commit()