from app.models.db_conn import DatabaseConnection
from datetime import datetime
import psycopg2

class Interventions(DatabaseConnection):

    def __init__(self):
        super().__init__()


    def update_intervention_comment(self, comment, incident_id):
        command = "UPDATE interventions SET comment = '%s' from incidents WHERE incident_id = '%s'" % (incident_id, comment)
        self.cursor.execute(command)
        return "intervention comment updated"


    def update_inter_location(self, inter_location, incident_id):
        command = "UPDATE interventions SET inter_location = '%s' from incidents WHERE incident_id = '%s'" % (incident_id, inter_location)
        self.cursor.execute(command)
        return "intervention comment updated"    


    def get_intervention(self, inter_id):
        command = """SELECT * from interventions cross join incidents WHERE inter_id ={}
        """.format(inter_id)
        self.cursor.execute(command)
        data = self.cursor.fetchone()
        print(data)
        return data


    def add_intervention(self, comment_by, redflag_id, comment, inter_location): 
        try:
            command = """INSERT INTO interventions (comment_by, redflag_id, comment, comment_type, inter_location, createdon) 
            VALUES('{}', '{}', '{}', '{}', '{}', '{}')
            """.format(comment_by, redflag_id, comment, "intervention", inter_location, datetime.now())
            self.cursor.execute(command)
            return "intervention added successfully"
        except psycopg2.IntegrityError:
            msg = "user_id or redflag_id doesnot exist , intervention not created"
            return msg


    def delete_intervention(self, inter_id):
        command = "DELETE from interventions WHERE inter_id = '%s'" % (inter_id)
        self.cursor.execute(command)
        return "inetervention deleted"


    def find_incident(self, incident_id):
        command = """
        SELECT * from incidents WHERE incident_id ={}
        """.format(incident_id)
        self.cursor.execute(command)
        data = self.cursor.fetchone()
        return data   

    def find_intervention(self, inter_id):
        command = """SELECT * from interventions WHERE inter_id ={}
        """.format(inter_id)
        self.cursor.execute(command)
        data = self.cursor.fetchone()
        return data          





    
