from flask import jsonify, request
import datetime
from app.models.interventions import Interventions
from app.views.validator import Validation
from app import app
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity,jwt_optional)
import os

interven = Interventions()
validate = Validation()
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'


@app.route('/api/v1/interventions', methods=['POST'])
@jwt_required
def add_intervention():
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised Access"}), 401

    input = request.get_json()
    validate_inputs = validate.input_data_validation(['redflag_id','inter_location','comment'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400

    datatype_validation = validate.validate_datatype(int, [input['redflag_id']])
    if datatype_validation:
        return jsonify({"status": 400, "error": datatype_validation}), 400
    
    createdby = current_user[0]
    incid = interven.create_intervention(
        current_user[0], 
        input['redflag_id'],  
        input['comment'], 
        input['inter_location']
        ) 
    return jsonify({"status": 201, "message": incid}), 201


@app.route('/api/v1/interventions/<int:inter_id>/<int:comment_by>/delete', methods=['DELETE'])
@jwt_required 
def delete_intervention(inter_id, comment_by):
    """enables user to delete a specific redflag"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised Access"}), 401

    intervention = interven.get_intervention(inter_id, comment_by)
    if not intervention:
        return jsonify({"status": 404, "error": "unable to find intervention"}), 404    
    else:
        incid = interven.intervention_deleted(inter_id, comment_by) 
        return jsonify({"status": 200, "data":[{"inter_id": inter_id, "comment_by": comment_by, "intervention": incid}]}), 200   



@app.route('/api/v1/interventions/<int:incident_id>/comment', methods=['PATCH'])
@jwt_required 
def edit_intervention(incident_id):
    """enables a user to edit an intervention"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised Access"}), 401

    input = request.get_json()
    validate_inputs = validate.input_data_validation(['comment'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400

    find_incident = interven.get_incident(incident_id)
    if not find_incident:
        return jsonify({"status": 404, "error": "unable to find incident or intervention"}), 404

    validate_status = validate.validate_status(find_incident[7])
    if validate_status:
        return validate_status
    else:
        Incid = interven.change_comment(incident_id, input["comment"])
        return jsonify({"status": 200, "redflag" : [{"incident_id": incident_id, "message": Incid}]}), 200


@app.route('/api/v1/interventions/<int:incident_id>/inter', methods=['PATCH'])
@jwt_required 
def change_inter_location(incident_id):
    """enables a user to change intervention coordinates"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised Access"}), 401

    input = request.get_json()
    validate_inputs = validate.input_data_validation(['inter_location'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400

    intervention = interven.get_incident(incident_id)
    if not intervention:
        return jsonify({"status": 404, "error": "unable to find incident or intervention"}), 404

    validate_status = validate.validate_status(intervention[7])
    if validate_status:
        return validate_status
    else:
        Incid = interven.update_inter_location(incident_id, input["inter_location"])
        return jsonify({"status": 200, "data" : [{"incident_id": incident_id, "intervention": Incid}]}), 200


@app.route('/api/v1/interventions', methods=['GET']) 
@jwt_required 
def view_all_interventions( ):
    """view all interventions"""
    current_user = get_jwt_identity()
    if current_user[8] == "user":
        return jsonify({"error": "Unauthorised access"}), 401

    interventions = interven.view_all_interventions() 
    inter_list = []
    for key in range(len(interventions)):
        inter_list.append({
            'inter_id': interventions[key][0],
            'comment_by':interventions[key][1],
            'redflag_id':interventions[key][2],
            'comment':interventions[key][3],
            'comment_type':interventions[key][4],
            'inter_location':interventions[key][5],
            'createdon':interventions[key][6]
        })
    return jsonify({"status": 200, "interventions": inter_list}), 200         


@app.route('/api/v1/users/interventions/<int:comment_by>', methods=['GET'])
@jwt_required 
def view_all_user_interventions(comment_by):
    """get all user's redflags/interventions"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised Access"}), 401
    else:
        interventions = interven.view_all_interventions_by_specific_user(comment_by)
        if not interventions:
            return jsonify({"status": 404, "error": "unable to find any intervention by you"}), 404 
        else:   
            new_list = []
            for key in range(len(interventions)):
                new_list.append({
                    'inter_id':interventions[key][0],
                    'comment_by':interventions[key][1], 
                    'redflag_id':interventions[key][2], 
                    'comment':interventions[key][3], 
                    'comment_type':interventions[key][4], 
                    'inter_location':interventions[key][5], 
                    'createdon':interventions[key][6]
                })
            return jsonify({"status": 200, "Interventions": new_list}), 200


@app.route('/api/v1/interventions/<int:inter_id>/<int:comment_by>', methods=['GET']) 
@jwt_required 
def find_one_intervention(inter_id, comment_by):
    """get a specific intervention"""
    current_user = get_jwt_identity()
    if current_user[8] == "admin":
        return jsonify({"error": "Unauthorised access"}), 401

    redflag = interven.get_intervention(inter_id, comment_by) 
    if not redflag:
        return jsonify({"status": 404, "error": "unable to find intervention"}), 404
    return jsonify({"status": 200, "redflag": {
        'inter_id': redflag[0],
        'comment_by':redflag[1],
        'redflag_id':redflag[2],
        'comment':redflag[3],
        'comment_type':redflag[4],
        'inter_location':redflag[5],
        'createdon':redflag[6]
    }}), 200



            


