from app.models.db_conn import DatabaseConnection
from datetime import datetime
import psycopg2

class Interventions(DatabaseConnection):

    def __init__(self):
        super().__init__()


    def change_comment(self, comment, incident_id, inter_id):
        command = "UPDATE interventions SET comment = '%s' from incidents WHERE incident_id = '%s' and inter_id = '%s'" % (comment, incident_id, inter_id)
        self.cursor.execute(command)
        return "intervention comment updated"


    def update_inter_location(self, location, incident_id, inter_id):
        command = "UPDATE interventions SET location = '%s' from incidents WHERE incident_id = '%s' and inter_id = '%s'" % (location, incident_id, inter_id)
        self.cursor.execute(command)
        return "intervention location comment updated"


    def create_intervention(self, comment_by, redflag_id, comment, location): 
        try:
            command = """INSERT INTO interventions (comment_by, redflag_id, comment, comment_type, location, createdon) 
            VALUES('{}', '{}', '{}', '{}', '{}', '{}')
            """.format(comment_by, redflag_id, comment, "intervention", location, datetime.now())
            self.cursor.execute(command)
            return "intervention added successfully"
        except psycopg2.IntegrityError:
            msg = "user_id or redflag_id doesnot exist , intervention not created"
            return msg


    def intervention_deleted(self, inter_id, comment_by):
        command = "DELETE from interventions WHERE inter_id = '%s' AND comment_by = '%s'" % (inter_id, comment_by)
        self.cursor.execute(command)
        return "inetervention deleted"


    def get_incident(self, incident_id):
        command = """SELECT * from incidents WHERE incident_id ='{}'
        """.format(incident_id)
        self.cursor.execute(command)
        incident = self.cursor.fetchone()
        return incident   

    def get_intervention(self, inter_id, comment_by):
        command = """SELECT * from interventions WHERE inter_id ='{}' and comment_by = '{}'
        """.format(inter_id, comment_by)
        self.cursor.execute(command)
        data = self.cursor.fetchone()
        return data 

    
    def check_intervention(self, inter_id):
        command = """SELECT * from interventions WHERE inter_id ='{}'
        """.format(inter_id)
        self.cursor.execute(command)
        data = self.cursor.fetchone()
        return data 


    def view_all_interventions_by_specific_user(self, comment_by):
        command = """SELECT * from interventions WHERE  comment_by = {}
        """.format(comment_by)
        self.cursor.execute(command)
        Interventions = self.cursor.fetchall()
        return Interventions           


    def view_all_interventions(self):
        command = """SELECT * FROM interventions
        """
        self.cursor.execute(command)
        Interventions = self.cursor.fetchall()
        return Interventions           






    
