from flask import jsonify

def api_response(success: bool, message: str, data=None, status_code = 200):
    response = {
        'success': success,
        'message': message,
        
    }
    
    if data is not None : 
        response['data'] = data
    
    return jsonify(response), status_code