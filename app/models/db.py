import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import RealDictCursor
from datetime import datetime

class DatabaseConnection:
 
    def __init__(self):
        self.db = 'ahmad'

        try:
            self.conn = psycopg2.connect(
            database=self.db, user="postgres", password="1988", port="5432", host="127.0.0.1"
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            self.dict_cursor = self.conn.cursor(
            cursor_factory=RealDictCursor)
            print("connected")
            print(self.db)

        except Exception as ex:
            print("connection failed {}".format(ex))


    def select_single_column(self, table, field, value):
        """Search specified table column with the value."""
        command = "SELECT * FROM %s WHERE %s = %s"
        self.dict_cursor.execute(command, (AsIs(table), AsIs(field), value))
        return self.dict_cursor.fetchall() 



class Migration(DatabaseConnection):
    
    def __init__(self):
        super().__init__()

    def drop_tables(self):
        commands = (
        """ 
        DROP TABLE users CASCADE
        """,
        """
        DROP TABLE incidents CASCADE
        """,
        """ 
        DROP TABLE interventions CASCADE
        """
        )
        for command in commands:
            self.cursor.execute(command)
    

    def create_tables(self):
        """ create tables in the PostgreSQL database"""
        commands = (
        """ CREATE TABLE IF NOT EXISTS USERS (
            ID SERIAL PRIMARY KEY UNIQUE,
            FIRST_NAME VARCHAR(50) NOT NULL,
            LAST_NAME VARCHAR(50) NOT NULL,
            OTHER_NAMES VARCHAR(50),
            EMAIL VARCHAR(50) UNIQUE,
            PASSWORD VARCHAR(50) NOT NULL,
            PHONE_NUMBER VARCHAR(50),
            USERNAME VARCHAR(50),
            ROLE VARCHAR(50) NOT NULL,
            createdOn timestamp(6) without time zone
            )
        """,
        """ CREATE TABLE IF NOT EXISTS INCIDENTS (
            ID SERIAL PRIMARY KEY UNIQUE,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES USERS(ID),
            DESCRIPTION VARCHAR(50) NOT NULL,
            COMMENT_TYPE VARCHAR(25) NOT NULL,
            location VARCHAR(50) NOT NULL,
            fromMyCamera VARCHAR(50),
            status VARCHAR(50) NOT NULL,
            createdOn timestamp(6) without time zone
            )
        """,
        """ CREATE TABLE IF NOT EXISTS INTERVENTIONS (
            INTER_ID  SERIAL PRIMARY KEY UNIQUE,
            COMMENT_BY INTEGER,
            FOREIGN KEY(COMMENT_BY) REFERENCES USERS(ID),
            REDFLAG_ID INTEGER,
            FOREIGN KEY(REDFLAG_ID) REFERENCES INCIDENTS(ID),
            COMMENT VARCHAR(50) NOT NULL,
            COMMENT_TYPE VARCHAR(50) NOT NULL,
            INTER_LOCATION VARCHAR(50) NOT NULL,
            createdOn timestamp(6) without time zone
            )
        """,    
        """ INSERT INTO USERS(first_name, last_name, email, password, role)VALUES('ahmad', 'kyakus', 'kyakuluahmed@gmail.com', 'ch1988', 'admin')
        """    
        )
        for command in commands: 
            try:
                self.cursor.execute(command)
            except psycopg2.IntegrityError as identifier:
                pass  


        
    
    

    

db_conn = Migration()
db_conn.create_tables() 
db_conn.drop_tables()
db_conn.create_tables()
# db_conn.add_human('name', 'address', 'age', 'single')
# db_conn.get_human(1)
# db_conn.update_address(1, 'jinja')
# db_conn.get_human(1)


# db_conn.add_simcard('ahmad','0782-192-133', 23401233,'vodafone', 123456)
# db_conn.get_simcard(1)
# db_conn.simcard_update(1, '0987654367')
# db_conn.get_simcard(1)
# db_conn.add_occupation_column_to_humans()
# db_conn.add_village_column_to_humans()


# # db_conn.delete_simcard(1)
# # db_conn.delete_human(1)





