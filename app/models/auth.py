from app.models.db_conn import DatabaseConnection
from datetime import datetime
import psycopg2

class User(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def register_user(self, first_name, last_name, email, password, isAdmin):
        command = """
        INSERT INTO USERS (first_name, last_name, email, password, isAdmin, createdon) VALUES('{}','{}','{}','{}','{}','{}')
        """.format(first_name, last_name, email, password, isAdmin, datetime.now())
        self.cursor.execute(command)
        return "user registered successfully"
    

    def user_login(self, email, password):
        command = """
        SELECT * FROM users WHERE email= '{}' AND password = '{}'
        """.format(email, password)
        self.cursor.execute(command)
        user1 = self.cursor.fetchone()
        return user1
        

     
    def get_user_by_email(self, email):
        command = """
        SELECT * FROM users WHERE email='{}'
        """.format(email)
        self.cursor.execute(command)
        user = self.cursor.fetchone()
        return user        
    

    

