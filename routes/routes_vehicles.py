from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from models import *
from config import db


vehicles_namespace = Namespace('vehicles', description='Endpoints pour les vehicles')


@vehicles_namespace.route("")
class VehiclesResource(Resource):
    def get(self):
        try:
            vehicles = Vehicles.get_all()
            vehicles_list = []
            for vehicle in vehicles:
                
                vehicles_list.append({
                    'idVehicle': vehicle.idVehicle,
                    'vehicleClass': vehicle.vehicleClass,
                    
                })

            return jsonify({'vehicles': vehicles_list})
        except Exception as e:
            return jsonify({'error': str(e)})

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


