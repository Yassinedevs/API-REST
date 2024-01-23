import pymysql
from config import mysql
from flask import jsonify
from flask import flash, request
from flask import Blueprint
from flask_restx import Resource, Namespace

vehicles_namespace = Namespace('vehicles', description='Endpoints pour les vehicles')


@vehicles_namespace.route("")
class VehiclesResource(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT vehicle_class FROM vehicles")
            film_rows = cursor.fetchall()

            if film_rows:
                response_data = {
                    "status": "success",
                    "message": "Liste de peoples récupérée avec succès.",
                    "data": film_rows
                }
                status_code = 200
            else:
                response_data = {
                    "status": "success",
                    "message": "Aucun vehicles trouvé.",
                    "data": []
                }
                status_code = 200
            
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Échec de la récupération de la liste des peoples.",
                "error_code": "INTERNAL_SERVER_ERROR",
                "details": str(e)
            }
            status_code = 500
        finally:
            cursor.close() 
            conn.close()  
        
        response = jsonify(response_data)
        response.status_code = status_code
        return response

    def post(self):
        return {"create":"a faire"}


@vehicles_namespace.route("/<int:id>")
class VehicleResource(Resource):
    def get(self, id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT vehicle_class FROM vehicles WHERE id = %s", (id,))
            film_rows = cursor.fetchall()

            if film_rows:
                response_data = {
                    "status": "success",
                    "message": "vehicles récupéré avec succès.",
                    "data": film_rows
                }
                status_code = 200
            else:
                response_data = {
                    "status": "success",
                    "message": "Aucun vehicles trouvé.",
                    "data": []
                }
                status_code = 200
            
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Échec de la récupération du film.",
                "error_code": "INTERNAL_SERVER_ERROR",
                "details": str(e)
            }
            status_code = 500
        finally:
            cursor.close() 
            conn.close()  
        
        response = jsonify(response_data)
        response.status_code = status_code
        return response

    def delete(self, id):
        return {"create":"a faire"}

    def put(self, id):
        return {"create":"a faire"}


