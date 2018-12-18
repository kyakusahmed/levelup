import psycopg2
from datetime import datetime

class DatabaseConnection:
 
    def __init__(self):
        self.db = ''

        try:
            self.conn = psycopg2.connect(
            database=self.db, user="", password="", port="5432", host=""
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            print("connected")
        except Exception as ex:
            print("connection failed {}".format(ex))


class Migration(DatabaseConnection):
    
    def __init__(self):
        super().__init__()

    def drop_tables(self):
        commands = (
        """ 
        DROP TABLE Humans CASCADE
        """,
        """
        DROP TABLE SimcardS CASCADE
        """
        )
        for command in commands:
            self.cursor.execute(command)
    

    def create_tables(self):
    
        """ create tables in the PostgreSQL database"""
        commands = (
        """ CREATE TABLE IF NOT EXISTS HUMANS (
            HUMAN_ID SERIAL PRIMARY KEY UNIQUE,
            NAME VARCHAR(50) NOT NULL UNIQUE,
            ADDRESS VARCHAR(50) NOT NULL,
            AGE VARCHAR(05),
            SINGLE VARCHAR(25) NOT NULL,
            CREATED_AT timestamp(6) without time zone
               )
        """,
        """ CREATE TABLE IF NOT EXISTS SIMCARDS (
            SIMCARD_ID  SERIAL PRIMARY KEY UNIQUE,
            ID INT NOT NULL,
            FOREIGN KEY(ID) REFERENCES HUMANS(HUMAN_ID),
            PHONE_NUMBER VARCHAR(50) NOT NULL,
            SERIAL VARCHAR(50) NOT NULL,
            SERVICE_PROVIDER VARCHAR(50) NOT NULL,
            is_active_human_id INT NOT NULL,
            CREATED_AT timestamp(6) without time zone
            )
        """
        )
        for command in commands:
            try:
                self.cursor.execute(command)
            except psycopg2.IntegrityError as identifier:
                pass  
        
    def add_human(self, name, address, age, single):
        try:
            command = """
            INSERT INTO HUMANS (name, address, age, single) VALUES('ahmad','lugazi','23','yes')
            """.format(name, address, age, single)
            self.cursor.execute(command)
            print("Human added successfully")
        except Exception as ex:
            return "failed {}".format(ex)

    def get_human(self, human_id):
        command = """
        SELECT * from humans WHERE name = 'ahmad'
        """.format(human_id)
        self.cursor.execute(command)
        data = self.cursor.fetchone()
        print(data) 

    def update_address(self, human_id, address):
        command = "UPDATE humans SET address = '%s' WHERE human_id = '%s'" % ('jinja', 1)
        self.cursor.execute(command)
        data =self.cursor.execute(command)
        print("address updated")

    def delete_human(self, human_id):
        command = """
        DELETE FROM HUMANS where human_id = {}
        """.format(human_id)
        self.cursor.execute(command)
        print("human deleted")


    def add_simcard(self, id, phone_number, serial, service_provider, is_active_human_id):
        try:
            command = """
            INSERT INTO simcards (id, phone_number, serial, service_provider, is_active_human_id) VALUES(1, '0782-192-133', 23401233,'vodafone', 123456)
            """.format(id, phone_number, serial, service_provider, is_active_human_id)
            self.cursor.execute(command)
            print("simcard added successfully")
        except Exception as ex:
            return "failed {}".format(ex)

    def get_simcard(self, simcard_id):
        command = """
        SELECT * from simcards WHERE simcard_id = {}
        """.format(simcard_id)
        self.cursor.execute(command)
        data = self.cursor.fetchone()
        print(data)

    def simcard_update(self, simcard_id, is_active_human_id):
        command = "UPDATE simcards SET is_active_human_id = '%s' WHERE simcard_id = '%s'" % (is_active_human_id, simcard_id)
        self.cursor.execute(command)
        data = self.cursor.execute(command)
        print('is_active_human_id is updated')
   
    def delete_simcard(self, simcard_id):
        command = """
        DELETE FROM simcards where simcard_id = {}
        """.format(simcard_id)
        self.cursor.execute(command)
        print("simcard deleted") 

    

db_conn = Migration()
db_conn.create_tables() 
db_conn.drop_tables()
db_conn.create_tables()
db_conn.add_human('name', 'address', 'age', 'single')
db_conn.get_human(1)
db_conn.update_address(1, 'jinja')
db_conn.get_human(1)


db_conn.add_simcard('ahmad','0782-192-133', 23401233,'vodafone', 123456)
db_conn.get_simcard(1)
db_conn.simcard_update(1, '0987654367')
db_conn.get_simcard(1)

db_conn.delete_simcard(1)
db_conn.delete_human(1)





