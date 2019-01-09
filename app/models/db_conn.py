import psycopg2
from datetime import datetime
import os

class DatabaseConnection:
 
    def __init__(self):
        if os.getenv('APP_SETTINGS') == 'testing':
            self.db = 'irep'
        else:
            self.db = 'ireporter'

        try:
            # self.conn = psycopg2.connect(
            # database="d7mcn5rj3q8pnl", user="zwypawrwvlinmw", password="29a416b2acdb956b73715f37028a7b5637f7e7c8f2d9b50908eddf1dd7458ef0", port="5432", host="ec2-107-21-93-132.compute-1.amazonaws.com"
            # )
            # self.conn.autocommit = True
            # self.cursor = self.conn.cursor()
            # print("connected")

            self.conn = psycopg2.connect(
            database=self.db, user="postgres", password="1988", port="5432", host="127.0.0.1"
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            print(self.db)
            location = 'lat,lng'
            splitted_location = location.split(',')
            print(splitted_location)
        except Exception as ex:
            print("connection failed {}".format(ex))
