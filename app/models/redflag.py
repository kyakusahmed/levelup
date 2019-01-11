from app.models.db_conn import DatabaseConnection
from datetime import datetime
import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import RealDictCursor


class Incident(DatabaseConnection):

    def __init__(self):
        super().__init__()

    def update_status(self, incident_id, status):
        command = "UPDATE incidents SET status = '%s' WHERE incident_id = '%s'" % (status, incident_id)
        self.cursor.execute(command)
        return "status updated" 
       

    def delete_redflag(self, incident_id):
        command = "DELETE from incidents CASCADE WHERE incident_id = '%s'" % (incident_id)
        self.cursor.execute(command)
        return "redflag deleted"


    def find_incident(self, incident_id):
        command = """
        SELECT * from incidents WHERE incident_id ={}
        """.format(incident_id)
        self.cursor.execute(command)
        data = self.cursor.fetchone()
        return data

    def incident_location_update(self, location, incident_id):
        command = "UPDATE incidents SET location = '%s' WHERE incident_id = '%s'" % (incident_id, location)
        self.cursor.execute(command)
        return "location updated" 


    def get_all_incidents_by_specific_user(self, createdby):
        command = """SELECT * FROM incidents WHERE user_id = '{}'
        """.format(createdby)
        self.cursor.execute(command)
        incidents = self.cursor.fetchall()
        return incidents
        

    def get_all_incidents(self):
        command = """SELECT * FROM incidents 
        """
        self.cursor.execute(command)
        results= self.cursor.fetchall()
        return results


    def add_redflag(self, createdby, description, location, fromMyCamera):
        command = """INSERT INTO incidents (user_id, description, comment_type, location, fromMyCamera, status, createdon) 
        VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(createdby, description, "redflag", location, fromMyCamera, "pending", datetime.now())
        self.cursor.execute(command)
        return "redflag added successfully"
    

    def update_description(self, description, incident_id):
        command = "UPDATE incidents SET description = '%s' WHERE incident_id = '%s'" % (incident_id, description)
        self.cursor.execute(command)
        return "description updated"