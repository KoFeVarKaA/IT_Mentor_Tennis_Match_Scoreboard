import json
import logging



class Responses():

    @staticmethod
    def success(data: bytes = None) -> dict:
        return {
            "data": data,
            "status_code": 200
        }
    
    @staticmethod
    def redirect(url: str) -> dict:
        return {
            "url": url,
            "status_code": 303
        }
    
    @staticmethod
    def input_err(data: bytes = None) -> dict:
        return {
            "data" : data,
            "status_code": 400
        }
    
    @staticmethod
    def not_found_err(data: bytes = None) -> dict:
        return {
            "data" : data,
            "status_code": 404
        }
    
    @staticmethod
    def already_exists(data: bytes = None) -> dict:
        return {
            "data" : data,
            "status_code": 409
        }

    @staticmethod
    def initial_err(data: bytes = None) -> dict:
        return {
            "data" : data,
            "status_code": 500
        }