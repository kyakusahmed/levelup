from flask import jsonify, request
import datetime
from app.models.auth import User
from app.views.validator import Validation
from app import app
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity,jwt_optional)
import os


user = User()
validate = Validation()
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'


@app.route('/api/v1/users/register', methods=['POST'])
def register_user():
    data = request.get_json()    
    val_input_data = validate.input_data_validation(['first_name', 'last_name', 'email', 'password'])
    if val_input_data:
        return jsonify({"status": 400, "error": val_input_data}), 400

    registered = user.get_user_by_email(data['email'])
    if registered:
        return jsonify({"status": 200, "message": "user registered already"}), 200
    else:
        get_input = request.get_json()
        role = get_input.get('role')
        roles = ["user","admin"]
        if not role in roles:
            return jsonify(message="role doesnt exist"), 406
        redflag = user.register_user(data["first_name"].strip(), data["last_name"].strip(),
            data["email"].strip(), data["password"].strip(), "user")
        return jsonify({"status": 201, "message": redflag}), 201


@app.route('/api/v1/users/login', methods=['POST'])
def user_login():

    validate_credentials = validate.input_data_validation(['email', 'password'])
    if validate_credentials:
        return jsonify({
            "status": 400, "error": validate_credentials
            }), 400

    data = request.get_json()
    check_user= user.user_login(
        data['email'], data['password'])
    if not check_user:
        return jsonify({"status": 200, "message": "register first"}), 200 

    access_token = create_access_token(identity=check_user)
    return jsonify({'message':"Login successful", 'access_token':access_token}), 200


@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user_to_admin(user_id):
    current_user = get_jwt_identity()
    if current_user[8] != "admin":
        return jsonify({
            "message": "Unauthorised Access"
            }), 401

    get_user = user.get_user_by_user_id(user_id)
    if not get_user:
        return jsonify(message="User Not Found"), 404
    else:
        get_input = request.get_json()
        role = get_input.get('role')
        roles = ["user","admin"]
        if not role in roles:
            return jsonify(message="role doesnt exist"), 406
        else:
            user.give_admin_rights_to_user(get_user[0], get_input['role'])
            return jsonify(message = "User is successfully given admin rights"), 200        
 

