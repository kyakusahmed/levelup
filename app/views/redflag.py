from app.models.redflag import Incident
from flask import jsonify, request, Flask

app = Flask(__name__)
incident = Incident()


@app.route('/api/v1/incidents', methods=['POST'])
def add_redflag():
    get_input = request.get_json()
    saved_redflag = incident.add_redflag(
        get_input['client_id'], get_input['description'], get_input['location'], get_input['fromMyCamera'])
    return jsonify({"status": 201, "message": saved_redflag}), 201


@app.route('/api/v1/users/incidents/<int:createdby>/<int:id>', methods=['GET'])
def get_specific_user_redflag(createdby, id):
    check_redflag = incident.get_specific_user_redflag(createdby, id)
    if not check_redflag:
        response = {"message": "redflag does not exist"}
    return jsonify({"status": 200, "user's_specific_redflag": check_redflag})


@app.route('/api/v1/users/incidents/<int:client_id>', methods=['GET'])
def get_all_user_redflags(client_id):
    search = incident.get_all_user_redflags(client_id)
    return jsonify({"status": 200, "all_user_redflags": search}), 200


@app.route('/api/v1/incidents', methods=['GET'])
def get_all_redflags():
    incidents = incident.get_all_redflags()
    return jsonify({"status": 200, "all_redflags_in_app": incidents}), 200


@app.route('/api/v1/incidents/<int:id>/update', methods=['PATCH'])
def update_redflag_description(id):


    search_incident = incident.find_incident(id)
    if not search_incident:
        return ({"status": 404, "error": "unable to find redflag"}), 404

    data = request.get_json()
    output = [{
        "message": incident.update_description(id, data['description']),
        "redflag_id": id
        }]
    return jsonify({"status": 200, "redflag": output})
       

   
    
