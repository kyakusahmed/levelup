from app.models.db_conn import DatabaseConnection
from datetime import datetime
import psycopg2

class User(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def register_user(self, first_name, last_name, email, password):
        command = """
        INSERT INTO USERS (first_name, last_name, email, password, role, createdon) VALUES('{}','{}','{}','{}','{}','{}')
        """.format(first_name, last_name, email, password, "user", datetime.now())
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


    def get_user_by_user_id(self, id):
        command = """SELECT * FROM users WHERE id ='{}'
        """.format(id)
        self.cursor.execute(command)
        user = self.cursor.fetchone()
        return user


    def give_admin_rights_to_user(self, id, role):
        command = "UPDATE users SET role = '%s' WHERE id = '%s'" % (role, id)
        self.cursor.execute(command)
        return "user is successfully given admin rights"
           
    

    

