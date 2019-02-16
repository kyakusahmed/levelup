from flask import jsonify, request
import datetime
from app.models.redflag import Incident
from app.views.validator import Validation
from app import app
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
import os
import smtplib
from app.views.sendmail import send_email
from flasgger import swag_from


incident = Incident()
validate = Validation()
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'


@app.route('/api/v1/incidents', methods=['POST'])
@jwt_required
@swag_from('../docs/add_redflag.yml') 
def add_incidet():
    
    current_user = get_jwt_identity()
    input = request.get_json()
    validate_inputs = validate.input_data_validation(['location', 'description'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400
        
    incid = incident.add_redflag(
        current_user[0],
        input['description'], 
        input['location'], 
        input['fromMyCamera']
        ) 
    return jsonify({"status": 201, "message": incid}), 201


@app.route('/api/v1/incidents/<int:incident_id>', methods=['GET']) 
@jwt_required 
def get_specific_redflag(incident_id):
    """get a specific redflag"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised Access"}), 401

    redflag = incident.find_incident(incident_id) 
    if not redflag:
        return jsonify({"status": 404, "error": "unable to find redflag"}), 404
    return jsonify({"status": 200, "redflag": {
        'incident_id': redflag[0],
        'createdby':redflag[1],
        'description':redflag[2],
        'comment_type':redflag[3],
        'location':redflag[4],
        'fromMyCamera':redflag[5],
        'status':redflag[6],
        'createdon':redflag[7]
    }}), 200



@app.route('/api/v1/incidents', methods=['GET'])
@jwt_required
@swag_from('../docs/admin_get_all_redflags.yml') 
def get_all_redflags( ):
    """get all redflags"""
    current_user = get_jwt_identity()
    if current_user[8] == "user":
        return jsonify({"error": "Unauthorised access"}), 401

    red_flag = incident.get_all_incidents() 
    incident_list = []
    for key in range(len(red_flag)):
        incident_list.append({'incident_id': red_flag[key][0], 'createdby':red_flag[key][1],
            'description':red_flag[key][2], 'comment_type':red_flag[key][3], 'location':red_flag[key][4],
            'fromMyCamera':red_flag[key][5], 'status':red_flag[key][6], 'createdon':red_flag[key][7]
        })
    return jsonify({"status": 200, "redflagss": incident_list}), 200 




@app.route('/api/v1/users/incidents/user', methods=['GET']) 
@jwt_required 
def get_all_user_redflags():
    """get all redflags"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised access"}), 401
        
    red_flag = incident.get_all_incidents_by_specific_user(current_user[0])
    if not red_flag:
        return jsonify({"status": 404, "error": "unable to find any incident created by you"}), 404
    incident_list = []
    for key in range(len(red_flag)):
        incident_list.append({
            'incident_id': red_flag[key][0],
            'createdby':red_flag[key][1],
            'description':red_flag[key][2],
            'comment_type':red_flag[key][3],
            'location':red_flag[key][4],
            'fromMyCamera':red_flag[key][5],
            'status':red_flag[key][6],
            'createdon':red_flag[key][7]
        })
    return jsonify({"status": 200, "redflagss": incident_list}), 200 




@app.route('/api/v1/incidents/<int:incident_id>/desc', methods=['PATCH'])
@jwt_required 
def edit_description(incident_id):
    """enables user to edit redflag"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised Access"}), 401

    input = request.get_json()
    validate_inputs = validate.input_data_validation(['description'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400

    redflag = incident.find_incident(incident_id)
    if not redflag:
        return jsonify({"status": 404, "error": "unable to find redflag"}), 404

    validate_status = validate.validate_status(redflag[6])
    if validate_status:
        return validate_status
    else:
        Incid = incident.update_description(incident_id, input["description"]) 
        return jsonify({"status": 200, "redflag" : [{"incident_id": incident_id, "message": Incid}]}), 200 


@app.route('/api/v1/incidents/<int:incident_id>/delete', methods=['DELETE'])
@jwt_required 
def delete_redflag(incident_id):
    """enables user to delete a specific redflag"""
    redflag = incident.find_incident(incident_id)
    if not redflag:
        return jsonify({"status": 404, "error": "unable to find redflag"}), 404    
    else:
        validate_status = validate.validate_status_delete(redflag[6])
        if validate_status:
            return validate_status

        delete_redflag = incident.delete_redflag(incident_id)
        return jsonify({"status": 200, "redflag": [{"incident_id": incident_id, "message": delete_redflag}]})


@app.route('/api/v1/incidents/<int:incident_id>/status', methods=['PATCH'])
@jwt_required 
def admin_updates_redflag_status(incident_id):
    """enables user to update specific redflag status"""
    current_user = get_jwt_identity()
    if current_user[8] != "admin":
        return jsonify({"error": "Unauthorised Access"}), 401

    input = request.get_json()
    validate_inputs = validate.input_data_validation(['status'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400

    redflag = incident.find_incident(incident_id)
    if not redflag:
        return jsonify({"status": 404, "error": "unable to find redflag"}), 404 

    validate_status = validate.validate_status(redflag[6])
    if validate_status:
        return validate_status
    
    status_updated = incident.update_status(incident_id, input['status'])

    subject = "Status Update"
    body = "Your iReporter Redflag status was updated"
    to_list = incident.get_user_by_id(redflag[1])[4]
    print(to_list)

    return jsonify({
        "status": 200, "redflag": [{"incident_id": redflag[0],"message": status_updated}],
        "message": send_email(to_list, subject, body)
        }), 200


@app.route('/api/v1/incidents/<int:incident_id>/location', methods=['PATCH'])
@jwt_required 
def update_location(incident_id):
    """enables user to update specific redflag location"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised Access"}), 401

    validate_inputs = validate.input_data_validation(['location'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400

    redflag = incident.find_incident(incident_id)
    if not redflag:
        return jsonify({"status": 404, "error": "unable to find redflag"}), 404 

    validate_status = validate.validate_status_location(redflag[6])
    if validate_status:
        return validate_status    
    
    input = request.get_json()
    location_updated = incident.incident_location_update(incident_id, input['location'])
    return jsonify({
        "status": 200,
        "redflag": [{"incident_id": redflag[0], "message": location_updated}]
        }), 200
    