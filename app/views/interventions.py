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
    if current_user[8] == True:
        return jsonify({"error": "Unauthorised Access for none user accounts"}), 401

    input = request.get_json()
    validate_inputs = validate.input_data_validation(['redflag_id','inter_location','comment'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400

    datatype_validation = validate.validate_datatype(int, [input['redflag_id']])
    if datatype_validation:
        return jsonify({"status": 400, "error": datatype_validation}), 400
    
    createdby = current_user[0]
    incid = interven.add_intervention(
        current_user[0], 
        input['redflag_id'],  
        input['comment'], 
        input['inter_location']
        ) 
    return jsonify({"status": 201, "message": incid}), 201


@app.route('/api/v1/interventions/<int:inter_id>/delete', methods=['DELETE'])
@jwt_required 
def delete_intervention(inter_id):
    """enables user to delete a specific redflag"""
    current_user = get_jwt_identity()
    if current_user[8] == True:
        return jsonify({"error": "Unauthorised Access for none user accounts"}), 401

    intervention = interven.find_intervention(inter_id)
    if not intervention:
        return jsonify({"status": 404, "error": "unable to find intervention"}), 404    
    else:
        if current_user[0] != intervention[1]:
            return jsonify({"status": 400, "error": "intervention does not belong to you"}), 400

        incid = interven.delete_intervention(inter_id)
        list = [{"inter_id": inter_id, "intervention": incid}] 
        return jsonify({"status": 200, "data": list})   



@app.route('/api/v1/interventions/<int:incident_id>/comment', methods=['PATCH'])
@jwt_required 
def edit_intervention(incident_id):
    """enables a user to edit an intervention"""
    current_user = get_jwt_identity()
    if current_user[8] == True:
        return jsonify({"error": "Unauthorised Access for none user accounts"}), 401

    input = request.get_json()
    validate_inputs = validate.input_data_validation(['comment'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400

    intervention = interven.find_incident(incident_id)
    if not intervention:
        return jsonify({"status": 404, "error": "unable to find incident or intervention"}), 404

    validate_status = validate.validate_status(intervention[7])
    if validate_status:
        return validate_status
    else:
        Incid = interven.update_intervention_comment(incident_id, input["comment"]) 
        list = [{"incident_id": incident_id, "intervention": Incid}]
        return jsonify({"status": 200, "data" : list}), 200


@app.route('/api/v1/interventions/<int:incident_id>/inter_location', methods=['PATCH'])
@jwt_required 
def update_inter_location(incident_id):
    """enables a user to edit an intervention"""
    current_user = get_jwt_identity()
    if current_user[8] == True:
        return jsonify({"error": "Unauthorised Access for none user accounts"}), 401

    input = request.get_json()
    validate_inputs = validate.input_data_validation(['inter_location'])
    if validate_inputs:
        return jsonify({"status": 400, "error": validate_inputs}), 400

    intervention = interven.find_incident(incident_id)
    if not intervention:
        return jsonify({"status": 404, "error": "unable to find incident or intervention"}), 404

    validate_status = validate.validate_status(intervention[7])
    if validate_status:
        return validate_status
    else:
        Incid = interven.update_inter_location(incident_id, input["inter_location"]) 
        list = [{"incident_id": incident_id, "intervention": Incid}]
        return jsonify({"status": 200, "data" : list}), 200

        


