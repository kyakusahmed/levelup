from flask import jsonify, request
from re import match

input_data = []

class Validation:
    """class for validating data"""
    def __init__(self):
        self.input_data = input_data

    def validate_datatype(self, data_type, input_data):
        """search for x and validate data type."""
        for x in input_data:
            try:
                int(x)
            except ValueError as error:
                return "Sorry {}. please enter an integer value {}".format(str(error), x)
        return None

    def input_data_validation(self, input_data):
        """Search for x and check if input is an empty string."""
        for x in input_data:
            input = request.get_json()
            message = x.strip() + ' is required'
            if not input[x]:
                return {'field': x, 'message': message}   
            elif x.strip() == 'email' and not bool(match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", input[x])):
                msg = 'invalid email'
                return ({'email': x, 'message': msg})
            elif x.strip() == 'password' and len(input[x].strip()) < 5:
                message = 'password should be atleast five characters'
                return message
            elif x.strip() == 'status' and input[x].strip() not in ['draft', 'resolved', 'under_investigation', 'rejected']:
                message = 'status doesnot exist, please use draft, resolved, rejected or under investigation'
                return message
            elif x.strip() == 'location' and not match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$", input[x]):    
                return 'invalid cordinates'
               
    def validate_status_delete(self, status):
        if status in ['rejected', 'resolved', 'under_investigation']:
            return jsonify({"status": 400, "error": "Unable to delete this redflag because its already " + status }), 400
        return None

    def validate_status_location(self, status):
        if status in ['rejected', 'resolved', 'under_investigation']:
            return jsonify({"status": 400, "error": "location cannot be changed because redflag its already " + status }), 400
        return None  

    def validate_status(self, status):
        if status in ['rejected', 'resolved']:
            return jsonify({
                "status": 400, "error": "field cannot be changed because redflag is already " + status }), 400
        return None