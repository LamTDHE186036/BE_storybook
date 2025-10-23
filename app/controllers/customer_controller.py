from app.utils.response import api_response
from flask import Blueprint, request, jsonify
from app.services.customer_services import CustomerService

class CustomerController:
    
    @staticmethod
    def get_customers(page, page_size, filters):
        try : 
            data, error = CustomerService.get_customers(page, page_size, filters=filters)
            if error :
                return api_response(
                    success=False,
                    message=f'Error getting customers: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Customers retrieved successfully',
                data=data,
                status_code=200
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
        
    @staticmethod
    def create_customer(request_data):
        try : 
            if not request_data :
                return api_response(
                    success=False,
                    message='Request data is required',
                    status_code=400
                )
            data, error = CustomerService.create_customer(request_data)
            if error :
                return api_response(
                    success=False,
                    message=f'Error creating customer: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Customer created successfully',
                data=data,
                status_code=201
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
            
    
    @staticmethod
    def update_customer(request_data):
        try : 
            if not request_data :
                return api_response(
                    success=False,
                    message='Request data is required',
                    status_code=400
                )
            data, error = CustomerService.update_customer(request_data)
            if error :
                return api_response(
                    success=False,
                    message=f'Error updating customer: {error}',
                    status_code=500
                )
            return api_response(
                success=True,
                message='Customer updated successfully',
                data=data,
                status_code=200
            )
        except Exception as e :
            return api_response(
                success=False,
                message=f'Internal server error: {str(e)}',
                status_code=500
            )
            
        