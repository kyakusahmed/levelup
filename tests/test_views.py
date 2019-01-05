import json
from .base_test import BaseTest


class UserTest(BaseTest):


    def test_user_register(self):
        """Test successful register"""
        regiseter_user = {
            "first_name":"ahmed",
            "last_name":"kyakus",
            "email": "kyakusahmed@out.com",
            "password": "1988ch",
            "isAdmin": False
        }
        response = self.app.post('/api/v1/users/register', json=regiseter_user)
        self.assertEqual(response.status_code, 201)
        assert json.loads(response.data)['data'] == "user registered successfully"

    def test_missing_fields(self):
        """Test register without data"""
        regiseter_user = {
            "first_name":"",
            "last_name":"kyakus",
            "email": "kyakusahmed@outlook.com",
            "password": "1988ch",
            "isAdmin": False
        }
        response = self.app.post('/api/v1/users/register', json=regiseter_user)
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['error']['message'] == 'first_name is required'

    def test_user_register_email_exist(self):
        """Test user email exists."""
        register_user = {
            "first_name":"avdb",
            "last_name":"kyakus",
            "email": "kyakusahmed@outlook.com",
            "password": "1988ch",
            "isAdmin": False
        }
        self.app.post('/api/v1/users/register', json=register_user)
        response = self.app.post('/api/v1/users/register', json=register_user)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "user registered already"

    def test_successful_user_login(self):
        """Test successful login."""
        register_user = {
            "first_name":"avdb",
            "last_name":"kyakus",
            "email": "kyakusahmed@outlook.com",
            "password": "1988ch",
            "isAdmin": False
        }
        self.app.post('/api/v1/users/register', json=register_user)
        response = self.app.post('/api/v1/users/login', json=register_user)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "Login successful"

    def test_user_not_registered(self):
        """Test missing login email and password."""
        register_user = {
            "email": "kyaku@outlook.com",
            "password": "1988fh"
        }
        response = self.app.post('/api/v1/users/login', json=register_user)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "register first"

    def test_invalid_email(self):
        register_user = {
            "email": "kyaku@outlook.",
            "password": "1988fh"
        }
        response = self.app.post('/api/v1/users/login', json=register_user)
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['error']['message'] == "invalid email"

    
    def test_password_too_short(self):
        register_user = {
            "first_name":"avdb",
            "last_name":"kyakus",
            "email": "kyaku@outlook.com",
            "password": "18fh",
            "isAdmin": False
        }
        response = self.app.post('/api/v1/users/register', json=register_user)
        self.assertEqual(response.status_code, 400)
        assert json.loads(response.data)['error'] == "password should be atleast five characters"



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
        self.assertEqual(response.status_code, 200)
            

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
        response = self.app.get('/api/v1/users/incidents/2', headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['status'] == 200

    def test_get_all_user_redflags_without_token(self):
        response = self.app.get('/api/v1/users/incidents/2')
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
        self.app.post('/api/v1/incidents', content_type="application/json", headers={"Authorization": "Bearer " + token}, json=redflag_Test)
        edit_data = {"description": "asVUYI516789"}
        response = self.app.patch('/api/v1/incidents/1/desc', headers={"Authorization": "Bearer " + token}, json=edit_data)
        assert response.status_code == 200
        assert json.loads(response.data)['redflag'][0]['message'] == "description updated"


    def test_update_location(self):
        token = self.return_user_token()
        redflag_Test = {
            "description": "aegrehjtr",
            "image": "5879p",
            "location": "setjyk",
            "video": "tfuyilt",
            "status": "pending"
        }
        self.app.post('/api/v1/incidents', content_type="application/json", headers={"Authorization": "Bearer " + token}, json=redflag_Test)
        location = {"location": "asVUYI516789"}
        response = self.app.patch('/api/v1/incidents/8/location', headers={"Authorization": "Bearer " + token}, json=location)
        print(response)
        assert response.status_code == 200
        assert json.loads(response.data)['redflag'][0]['message'] == "location updated"    


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
        response = self.app.delete('/api/v1/incidents/2/delete', headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        print(data)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['redflag'][0]['message'] == "redflag deleted"

    
    def test_delete_redflag_not_found(self):
        token = self.return_user_token()
        response = self.app.delete('/api/v1/incidents/12345/delete', headers={"Authorization": "Bearer " + token})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        assert json.loads(response.data)['error'] == "unable to find redflag"


    def test_admin_updates_redflag_status_without_token(self):
        status_update = {"status": "under_investigation"}
        response = self.app.patch('/api/v1/incidents/1/status', json=status_update)
        assert response.status_code == 401
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"


    def test_admin_update_redflag_status_not_found(self):
        token = self.return_admin_token()
        status_update = {"status": "under_investigation"}
        response = self.app.patch('/api/v1/incidents/11111/status', headers={"Authorization": "Bearer " + token}, json=status_update)
        assert response.status_code == 404
        assert json.loads(response.data)['error'] == "unable to find redflag"

    def test_admin_update_redflag_status(self):
        token = self.return_user_token()
        redflag_test = {
            "description": "aegrehjtr",
            "image": "",
            "location": "setjyk",
            "video": "",
            "status": "pending"
        }
        self.app.post('/api/v1/incidents', headers={"Authorization": "Bearer " + token}, json=redflag_test)
        token = self.return_admin_token()
        status_update = {"status": "under_investigation"}
        response = self.app.patch('/api/v1/incidents/1/status', headers={"Authorization": "Bearer " + token}, json=status_update)
        assert response.status_code == 200
        assert json.loads(response.data)['redflag'][0]['message'] == "status updated"    



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


    def test_add_intervention_redflag_id_doesnot_exist(self):
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


    def test_edit_comment_comment_missing(self):
        token = self.return_user_token()
        test_data = {
            "redflag_id": 1,
            "comment": "wevlqnwcAOP",
            "inter_location": "0.5, 32.5"
        }
        self.app.post('/api/v1/interventions', content_type="application/json", 
        headers={"Authorization": "Bearer " + token}, json=test_data)
        update_comment = {"comment": ""}
        response = self.app.patch('/api/v1/interventions/1/comment', 
        headers={"Authorization": "Bearer " + token}, json=update_comment)
        assert response.status_code == 400
        assert json.loads(response.data)['error']['message'] == "comment is required"
   
   
    def test_edit_comment_comment_missing_without_token(self):
        update_comment = {"comment": ""}
        response = self.app.patch('/api/v1/interventions/1/comment', json=update_comment)
        assert response.status_code == 401
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"


    def test_delete_intervention(self):
        token = self.return_user_token()
        test_data = {
            "redflag_id": 1,
            "comment": "wevlqnwcAOP",
            "inter_location": "0.5, 32.5"
        }
        self.app.post('/api/v1/interventions', content_type="application/json", 
        headers={"Authorization": "Bearer " + token}, json=test_data)
        response = self.app.delete('/api/v1/interventions/1/2/delete', 
        headers={"Authorization": "Bearer " + token})
        assert response.status_code == 200


    def test_delete_intervention_without_token(self):
        test_data = {
            "redflag_id": 1,
            "comment": "wevlqnwcAOP",
            "inter_location": "0.5, 32.5"
        }
        self.app.post('/api/v1/interventions', content_type="application/json", json=test_data)
        response = self.app.delete('/api/v1/interventions/1/2/delete')
        assert response.status_code == 401
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"


    def test_change_inter_location(self):
        token = self.return_user_token()
        test_data = {
            "redflag_id": 1,
            "comment": "wevlqnwcAOP",
            "inter_location": "0.5, 32.5"
        }
        self.app.post('/api/v1/interventions', content_type="application/json", 
        headers={"Authorization": "Bearer " + token}, json=test_data)
        update_location = {"inter_location": "0.5, 32.9"}
        response = self.app.patch('/api/v1/interventions/1/inter', 
        headers={"Authorization": "Bearer " + token}, json=update_location)
        assert response.status_code == 200
        assert json.loads(response.data)['data'][0]['intervention'] == "intervention comment updated"


    def test_view_all_interventions(self):
        admin_token = self.return_admin_token()
        token = self.return_user_token()
        test_data = {
            "redflag_id": 1,
            "comment": "wevlqnwcAOP",
            "inter_location": "0.5, 32.5"
        }
        self.app.post('/api/v1/interventions', content_type="application/json", 
        headers={"Authorization": "Bearer " + token}, json=test_data)
        response = self.app.get(
            '/api/v1/interventions', headers={"Authorization": "Bearer " + admin_token})
        assert response.status_code == 200


    def test_view_all_interventions_without_token(self):
        test_data = {
            "redflag_id": 1,
            "comment": "wevlqnwcAOP",
            "inter_location": "0.5, 32.5"
        }
        self.app.post('/api/v1/interventions', content_type="application/json", json=test_data)
        response = self.app.get('/api/v1/interventions')
        assert response.status_code == 401
        assert json.loads(response.data)['msg'] == "Missing Authorization Header"


    def test_view_all_user_interventions(self):
        token = self.return_user_token()
        test_data = {
            "redflag_id": 1,
            "comment": "wevlqnwcAOP",
            "inter_location": "0.5, 32.5"
        }
        self.app.post(
            '/api/v1/interventions', content_type="application/json",
            headers={"Authorization": "Bearer " + token}, json=test_data
            )
        response = self.app.get(
            '/api/v1/users/interventions/2', content_type="application/json",
            headers={"Authorization": "Bearer " + token})
        assert response.status_code == 200


    def test_view_all_user_interventions_without_token(self):
        test_data = {
            "redflag_id": 1,
            "comment": "wevlqnwcAOP",
            "inter_location": "0.5, 32.5"
        }
        self.app.post('/api/v1/interventions', content_type="application/json", json=test_data)
        response = self.app.get('/api/v1/users/interventions/2')
        assert response.status_code == 401


    def test_find_one_intervention(self):
        token = self.return_user_token()
        test_data = {
            "redflag_id": 1,
            "comment": "wevlqnwcAOP",
            "inter_location": "0.5, 32.5"
        }
        self.app.post(
            '/api/v1/interventions', content_type="application/json",
            headers={"Authorization": "Bearer " + token}, json=test_data
            )
        response = self.app.get(
            '/api/v1/interventions/4/2', content_type="application/json",
            headers={"Authorization": "Bearer " + token})
        assert response.status_code == 200
    

        

