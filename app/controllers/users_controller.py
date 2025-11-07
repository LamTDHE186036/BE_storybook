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
        
            
    @staticmethod
    def get_users(): 
        try:
            data, error = UsersServices.get_users()
            if error:
                return api_response(
                    success=False,
                    message=f'Error fetching users: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Users fetched successfully',
                data=data,
                status_code=200
            )
            
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
            
    
    @staticmethod
    def update_user(response_data):
        try:
            data, error = UsersServices.update_user(response_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error updating user: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='User updated successfully',
                data=data,
                status_code=200
            )
            
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
    
    
    @staticmethod
    def delete_user(user_id):
        try:
            data, error = UsersServices.delete_user(user_id)
            if error:
                return api_response(
                    success=False,
                    message=f'Error deleting user: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='User deleted successfully',
                data=data,
                status_code=200
            )
            
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
            
            
    @staticmethod
    def delete_multiple_users(response_data):
        try:
            data, error = UsersServices.delete_multiple_users(response_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error deleting users: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Users deleted successfully',
                data=data,
                status_code=200
            )
            
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
    
    @staticmethod
    def forgot_password(response_data) :
        try:
            data, error = UsersServices.forgot_password(response_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error in forgot password process: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Password reset link sent successfully',
                data=data,
                status_code=200
            )
            
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
            
    @staticmethod
    def confirm_otp(response_data) :
        try:
            data, error = UsersServices.confirm_otp(response_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error confirming OTP: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='OTP confirmed successfully',
                data=data,
                status_code=200
            )
            
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
    @staticmethod
    def reset_password(response_data) :
        try:
            data, error = UsersServices.reset_password(response_data)
            if error:
                return api_response(
                    success=False,
                    message=f'Error resetting password: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Password reset successfully',
                data=data,
                status_code=200
            )
            
        except Exception as e:
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )