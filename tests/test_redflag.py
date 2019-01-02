import json
from .base_test import BaseTest


class IncidentTest(BaseTest):


    def test_add_incident(self):
        """Test successful register"""
        token = self.return_user_token()
        incident_Test = {
            "description": "w3y45u w4u5ik 5w5i63",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        response = self.app.post('/api/v1/incidents', headers={"Authorization": "Bearer " + token}, json=incident_Test)
        self.assertEqual(response.status_code, 201)
        assert json.loads(response.data)['message'] == "redflag added successfully"
        assert json.loads(response.data)['status'] == 201


    def test_description_is_missing(self):
        """Test successful register"""
        token = self.return_user_token()
        incident_Test = {
            "description": "",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        response = self.app.post('/api/v1/incidents', headers={"Authorization": "Bearer " + token}, json=incident_Test)
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['error']['message'] == "description is required"
        assert json.loads(response.data)['error']['field'] == "description"
        assert json.loads(response.data)['status'] == 400


    def test_add_incident_with_out_token(self):
        """Test successful register"""
        incident_Test = {
            "description": "",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        response = self.app.post('/api/v1/incidents', json=incident_Test)
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"


    def test_get_specific_redflag_without_token(self):
        redflag_Test = {
            "description": "",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        self.app.post('/api/v1/incidents', json=redflag_Test)
        response = self.app.get('/api/v1/incidents/1')
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"


    def test_get_specific_redflag(self):
        token = self.return_user_token()
        redflag_Test = {
            "description": "sbaebab",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        self.app.post('/api/v1/incidents', headers={"Authorization": "Bearer " + token}, json=redflag_Test)
        response = self.app.get('/api/v1/incidents/1', headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        # self.assertIsInstance(data['redflag'], dict)
            

    def test_get_specific_redflag_not_found(self):
        token = self.return_user_token()
        response = self.app.get('/api/v1/incidents/1500', headers={"Authorization": "Bearer " + token})
        self.assertEqual(response.status_code, 404)
        assert json.loads(response.data)['error'] == "unable to find redflag"


    def test_get_redflags_with_user_token(self):
        token = self.return_user_token()
        redflag_Test = {
            "description": "aegrehjtr",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        self.app.post('/api/v1/incidents', headers={"Authorization": "Bearer " + token}, json=redflag_Test)
        response = self.app.get('/api/v1/incidents', headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['error'] == "Unauthorised access"    


    def test_get_all_user_redflags(self):
        token = self.return_user_token()
        redflag_Test = {
            "description": "aegrehjtr",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        self.app.post('/api/v1/incidents', headers={"Authorization": "Bearer " + token}, json=redflag_Test)
        response = self.app.get('/api/v1/incidents/users/2', headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['status'] == 200
        self.assertIsInstance(data['redflags'], list) 


    def test_get_all_user_redflags_without_token(self):
        response = self.app.get('/api/v1/incidents/users/2')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"


    def test_edit_description(self):
        token = self.return_user_token()
        redflag_Test = {
            "description": "aegrehjtr",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        self.app.post('/api/v1/incidents', headers={"Authorization": "Bearer " + token}, json=redflag_Test)
        edit_data = {"description": "asVUYI516789"}
        response = self.app.patch('/api/v1/incidents/1/desc', headers={"Authorization": "Bearer " + token}, json=edit_data)
        assert response.status_code == 200
        assert json.loads(response.data)['redflag'][0]['message'] == "description updated"


    def test_edit_description_without_token(self):
        redflag_Test = {
            "description": "aegrehjtr",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        self.app.post('/api/v1/incidents', json=redflag_Test)
        edit_data = {"description": "asVUYI516789"}
        response = self.app.patch('/api/v1/incidents/1/desc', json=edit_data)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"


    def test_edit_description_incident_not_found(self):
        token = self.return_user_token()
        edit_data = {"description": "asVUYI516789"}
        response = self.app.patch('/api/v1/incidents/4000/desc', headers={"Authorization": "Bearer " + token}, json=edit_data)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        assert json.loads(response.data)['error'] == "unable to find redflag"


    def test_delete_redflag(self):
        token = self.return_user_token()
        redflag_Test = {
            "description": "aegrehjtr",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        self.app.post('/api/v1/incidents', headers={"Authorization": "Bearer " + token}, json=redflag_Test)
        response = self.app.delete('/api/v1/incidents/1/delete', headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['redflag'][0]['message'] == "redflag deleted"

    
    def test_delete_redflag_not_found(self):
        token = self.return_user_token()
        response = self.app.delete('/api/v1/incidents/12345/delete', headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        assert json.loads(response.data)['error'] == "unable to find redflag"


    def test_admin_updates_redflag_status(self):
        user_token = self.return_user_token()
        token = self.return_admin_token()
        redflag_Test = {
            "description": "aegrehjtr",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        self.app.post('/api/v1/incidents', headers={"Authorization": "Bearer " + user_token}, json=redflag_Test)
        status_update = {"status": "under_investigation"}
        response = self.app.patch('/api/v1/incidents/1/status', headers={"Authorization": "Bearer " + token}, json=status_update)
        assert response.status_code == 200
        assert json.loads(response.data)['redflag'][0]['message'] == "status updated"


    



