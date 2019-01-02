import json
from .base_test import BaseTest


class InterventionsTest(BaseTest):

    
    def test_add_intervention(self):
        """Test intervention is added successfully"""
        token = self.return_user_token()
        incident_Test = {
            "description": "w3y45u w4u5ik 5w5i63",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        response = self.app.post('/api/v1/incidents', headers={"Authorization": "Bearer " + token}, json=incident_Test)
        test_data = {
            "redflag_id": 1,
            "comment": "rctyhvubinoui",
            "inter_location": "0.5, 32.5"
        }
        response = self.app.post('/api/v1/interventions', 
        headers={"Authorization": "Bearer " + token}, json=test_data)
        self.assertEqual(response.status_code, 201)
        assert json.loads(response.data)['message'] == "intervention added successfully"
        assert json.loads(response.data)['status'] == 201


    def test_add_inyervention_redflag_id_doesnot_exist(self):
        """Test with redflag_id which doesnot exist"""
        token = self.return_user_token()
        test_data = {
            "redflag_id": 10,
            "comment": "rctyhvubinoui",
            "inter_location": "0.5, 32.5"
        }
        response = self.app.post('/api/v1/interventions', 
        headers={"Authorization": "Bearer " + token}, json=test_data)
        self.assertEqual(response.status_code, 201)
        assert json.loads(response.data)['message'] == "user_id or redflag_id doesnot exist , intervention not created"
        assert json.loads(response.data)['status'] == 201
    


    def test_comment_is_missing(self):
        """Test comment field is missing"""
        token = self.return_user_token()
        test_data = {
            "redflag_id": 10,
            "comment": "",
            "inter_location": "0.5, 32.5"
        }
        response = self.app.post('/api/v1/interventions', headers={"Authorization": "Bearer " + token}, json=test_data)
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['error']['message'] == "comment is required"
        assert json.loads(response.data)['error']['field'] == "comment"
        assert json.loads(response.data)['status'] == 400


    def test_add_intervention_with_out_token(self):
        """Test successful register"""
        test_data = {
            "redflag_id": 10,
            "comment": "ewrtry",
            "inter_location": "0.5, 32.5"
        }
        response = self.app.post('/api/v1/interventions', json=test_data)
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"


    def test_edit_comment(self):
        token = self.return_user_token()
        test_data = {
            "redflag_id": 1,
            "comment": "wevlqnwcAOP",
            "inter_location": "0.5, 32.5"
        }
        self.app.post('/api/v1/interventions', content_type="application/json", 
        headers={"Authorization": "Bearer " + token}, json=test_data)
        update_comment = {"comment": "asVUYI516789"}
        response = self.app.patch('/api/v1/interventions/1/comment', 
        headers={"Authorization": "Bearer " + token}, json=update_comment)
        assert response.status_code == 200
        assert json.loads(response.data)['redflag'][0]['message'] == "intervention comment updated"
   