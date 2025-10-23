from app.utils.response import api_response
from app.services.users_servieces import UsersServices
from flask import request, jsonify, g
import json

class UsersController:
    @staticmethod
    def register(response_data):
        try:
            data, error = UsersServices.register(response_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error registering user: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='User registered successfully',
                data=data,
                status_code=201
            )
            
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
            
    @staticmethod
    def login(response_data):
        try:
            print("íads")
            token = None
            print(json.dumps(dict(request.headers), indent=2, ensure_ascii=False))   
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            print("íads 222")
            data, error = UsersServices.login(response_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error logging in: {error}',
                    status_code=401
                )
            return api_response(
                success=True,
                message='Login successful',
                data=data,
                status_code=200
            )
            
        except Exception as e:
            print(e)
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
        
            