from app.models.db import DatabaseConnection
from datetime import datetime
import psycopg2
from psycopg2.extensions import AsIs


class Incident(DatabaseConnection):
    
    def __init__(self):
        super().__init__()


    def add_redflag(self, client_id, description, location, fromMyCamera):
        """Create new Order."""
        command = """INSERT INTO incidents (user_id, description, comment_type, location, fromMyCamera, status, createdon) 
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        self.cursor.execute(command, (
            client_id, description, "redflag", location, fromMyCamera, "pending", str(datetime.now())))
        return "Redflag added Successfully"


    def get_all_user_redflags(self, client_id):
        """get all user redflags."""
        return self.select_single_column('incidents', 'user_id', client_id)


    def get_all_redflags(self):
        """admin gets all redflags in the app."""
        command = """SELECT * FROM incidents"""
        self.dict_cursor.execute(command)
        return self.dict_cursor.fetchall()


    def get_specific_user_redflag(self, client_id, id):
        """Get a specific order for a client."""
        command = """SELECT * FROM incidents WHERE id = %s AND user_id = %s;"""
        self.dict_cursor.execute(command, (id, client_id))
        redflags = self.dict_cursor.fetchall()
        return redflags


    def update_description(self, description, id):
        command = """UPDATE incidents SET description = %s WHERE id = %s
        """
        self.cursor.execute(command,(id, description))
        return "Redflag description updated"


    def find_incident(self, incident_id):
        command = """SELECT * from incidents WHERE id = {}
        """.format(incident_id)
        self.cursor.execute(command)
        data = self.cursor.fetchone()
        return data
      
