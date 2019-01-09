from flask import jsonify, request
import datetime
from app.models.redflag import Incident
from app.models.auth import User
from app.views.validator import Validation
from app import app
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
import os
import smtplib

user = User()
incident = Incident()
validate = Validation()
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'


@app.route('/api/v1/incidents', methods=['POST'])
@jwt_required
def add_incidet():
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised Access"}), 401

    input = request.get_json()
    validate_inputs = validate.input_data_validation(['location','description'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400

    # validate_location = validate.location_validate(['location'])
    # if validate_location:
    #     return jsonify({"status": 400, "error": validate_location}), 400     
    
    createdby = current_user[0]
    incid = incident.add_redflag(
        current_user[0], 
        input['description'], 
        input['location'], 
        input['image'], 
        input['video']
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
        'comment':redflag[2],
        'comment_type':redflag[3],
        'location':redflag[4],
        'image':redflag[5],
        'video':redflag[6],
        'status':redflag[7],
        'createdon':redflag[8]
    }}), 200


@app.route('/api/v1/incidents', methods=['GET']) 
@jwt_required
def get_all_redflag( ):
    """get all redflags"""
    current_user = get_jwt_identity()
    if current_user[8] == "user":
        return jsonify({"error": "Unauthorised access"}), 401

    red_flag = incident.get_all_incidents() 
    incident_list = []
    for key in range(len(red_flag)):
        incident_list.append({
            'incident_id': red_flag[key][0],
            'createdby':red_flag[key][1],
            'comment':red_flag[key][2],
            'comment_type':red_flag[key][3],
            'location':red_flag[key][4],
            'image':red_flag[key][5],
            'video':red_flag[key][6],
            'status':red_flag[key][7],
            'createdon':red_flag[key][8]
        })
    return jsonify({"status": 200, "redflagss": incident_list}), 200 


@app.route('/api/v1/users/incidents/<int:createdby>', methods=['GET']) 
@jwt_required 
def get_all_user_redflags(createdby):
    """get all redflags"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised access"}), 401
    else:
        red_flag = incident.get_all_incidents_by_specific_user(createdby)
        if not red_flag:
            return jsonify({"status": 404, "error": "unable to find any incident created by you"}), 404
        incident_list = []
        for key in range(len(red_flag)):
            incident_list.append({
                'incident_id': red_flag[key][0],
                'createdby':red_flag[key][1],
                'comment':red_flag[key][2],
                'comment_type':red_flag[key][3],
                'location':red_flag[key][4],
                'image':red_flag[key][5],
                'video':red_flag[key][6],
                'status':red_flag[key][7],
                'createdon':red_flag[key][8]
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

    validate_status = validate.validate_status(redflag[7])
    if validate_status:
        return validate_status
    else:
        Incid = incident.update_description(incident_id, input["description"]) 
        return jsonify({"status": 200, "redflag" : [{"incident_id": incident_id, "message": Incid}]}), 200 


@app.route('/api/v1/incidents/<int:incident_id>/delete', methods=['DELETE'])
@jwt_required 
def delete_redflag(incident_id):
    """enables user to delete a specific redflag"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised Access"}), 401

    redflag = incident.find_incident(incident_id)
    if not redflag:
        return jsonify({"status": 404, "error": "unable to find redflag"}), 404    
    else:
        validate_status = validate.validate_status_delete(redflag[7])
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

    validate_status = validate.validate_status(redflag[7])
    if validate_status:
        return validate_status 

    # host = "smtp.gmail.com"
    # port = 587
    # username = "kyakuluahmed@gmail.com"
    # password = "CHRISTINE77"
    # from_email = username
    # current_user = get_jwt_identity()
    # to_list = [current_user[4]]

    # email_conn = smtplib.SMTP(host, port)
    # email_conn.ehlo()
    # email_conn.starttls()
    # email_conn.login(username, password)
    # email_conn.sendmail(from_email, to_list, "your redflag status was updated")
    
    status_updated = incident.update_status(incident_id, input['status'])
    return jsonify({"status": 200, "redflag": [{"incident_id": redflag[0],"message": status_updated}]}), 200


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

    validate_status = validate.validate_status_location(redflag[7])
    if validate_status:
        return validate_status    
    
    input = request.get_json()
    location_updated = incident.incident_location_update(incident_id, input['location'])
    return jsonify({
        "status": 200,
        "redflag": [{"incident_id": redflag[0], "message": location_updated}]
        }), 200
    