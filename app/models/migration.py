from app.models.db_conn import DatabaseConnection
import psycopg2

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
            USER_ID SERIAL PRIMARY KEY UNIQUE,
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
            INCIDENT_ID  SERIAL PRIMARY KEY UNIQUE,
            createdBy INTEGER,
            FOREIGN KEY(createdBy) REFERENCES USERS(USER_ID),
            DESCRIPTION VARCHAR(50) NOT NULL,
            COMMENT_TYPE VARCHAR(25) NOT NULL,
            location VARCHAR(50) NOT NULL,
            image VARCHAR(50),
            video VARCHAR(50),
            status VARCHAR(50) NOT NULL,
            createdOn timestamp(6) without time zone
            )
        """,
        """ CREATE TABLE IF NOT EXISTS INTERVENTIONS (
            INTER_ID  SERIAL PRIMARY KEY UNIQUE,
            COMMENT_BY INTEGER,
            FOREIGN KEY(COMMENT_BY) REFERENCES USERS(USER_ID),
            REDFLAG_ID INTEGER,
            FOREIGN KEY(REDFLAG_ID) REFERENCES INCIDENTS(INCIDENT_ID),
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


# db = Migration()
# # db.create_tables()
# db.drop_tables() 
# # db.create_tables()               