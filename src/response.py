import json
import logging



class Responses():

    @staticmethod
    def success(data: dict = None):
        return {
            "data": data,
            "status_code": 200
        }
    
    @staticmethod
    def input_err(message: str):
        return {
            "data" : {"message": message},
            "status_code": 400
        }
    
    @staticmethod
    def not_found_err(message: str):
        return {
            "data" : {"message": message},
            "status_code": 404
        }
    
    @staticmethod
    def already_exists(message: str):
        return {
            "data" : {"message": message},
            "status_code": 409
        }

    @staticmethod
    def initial_err(message: str):
        return {
            "data" : {"message": message},
            "status_code": 500
        }