from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace, fields
from models import *
from config import db
from flask_jwt_extended import jwt_required

vehicles_namespace = Namespace('vehicles', description='Endpoints pour les vehicles')

vehicle_model = vehicles_namespace.model('Vehicles', {
    'vehicleClass': fields.String(description='vehicleClass'),

})

@vehicles_namespace.route("")
class VehiclesResource(Resource):
    @jwt_required()
    @vehicles_namespace.doc(security="JsonWebToken") 
    def get(self):
        try:
            vehicles = Vehicles.get_all()
            vehicles_list = []
            for vehicle in vehicles:
                
                vehicles_list.append({
                    'idVehicle': vehicle.idVehicle,
                    'vehicleClass': vehicle.vehicleClass,
                    
                })

            response_data = {
                "status": "success",
                "action": "Lister les vehicles",
                "data": vehicles_list
                }
                    
            return make_response(jsonify(response_data), 200)
        except Exception as e:
            response_data = {
                "status": "error",
                "action": "Lister les vehicles",
                "error": str(e)
                }
                    
            return make_response(jsonify(response_data), 400)
    
    @jwt_required()
    @vehicles_namespace.doc(security="JsonWebToken") 
    @vehicles_namespace.expect(vehicle_model)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            new_vehicle = Vehicles(
                vehicleClass=json_data.get('vehicleClass'),

            )
            db.session.add(new_vehicle)
            db.session.commit()

            response_data = {
                "status": "success",
                "action": "Lister les vehicles",
                "data": new_vehicle
                }
                    
            return make_response(jsonify(response_data), 200)
        except Exception as e:
            response_data = {
                "status": "error",
                "action": "Lister les vehicles",
                "error": str(e)
                }
                    
            return make_response(jsonify(response_data), 200)
        


@vehicles_namespace.route("/<int:id>")
class VehicleResource(Resource):
    @jwt_required()
    @vehicles_namespace.doc(security="JsonWebToken") 
    def get(self, id):
        try:
            vehicles = Vehicles.get_one_by_id(id)
            if vehicles:
                vehicle_data = {
                    'idVehicle': vehicles.idVehicle,
                    'vehicleClass': vehicles.vehicleClass,
                    }
                response_data = {
                    "status": "success",
                    "action": "Lister les vehicles",
                    "data": vehicle_data
                }
                    
                return make_response(jsonify(response_data), 200)
            else:
                response_data = {
                "status": "success",
                "action": "Lister les vehicles",
                "data": "Pas de vehicle"
                }
                    
            return make_response(jsonify(response_data), 400)

           
        except Exception as e:
            response_data = {
                "status": "error",
                "action": "Lister les vehicles",
                "error": str(e)
                }
                    
            return make_response(jsonify(response_data), 400)
    
    @jwt_required()
    @vehicles_namespace.doc(security="JsonWebToken") 
    def delete(self, id):
        try:
            existing_vehicle = Vehicles.get_one_by_id(id)

            if existing_vehicle:
                db.session.delete(existing_vehicle)
                db.session.commit()

                response_data = {
                        "status": "success",
                        "action": "vehicle supprimé",
                        
                    }
                    
                return make_response(jsonify(response_data), 200)
            else:
                response_data = {
                        "status": "error",
                        "action": "vehicle supprimé",
                        "error": "Vehicle not found"
                    }
                    
                return make_response(jsonify(response_data), 400)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Vehicle supprimé",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)
    
    @jwt_required()
    @vehicles_namespace.doc(security="JsonWebToken") 
    @vehicles_namespace.expect(vehicle_model)
    def post(self, id):
        try:
            json_data = request.get_json(force=True)
            vehicle = Vehicles.get_one_by_id(id)

            if not vehicle:
                response_data = {
                        "status": "error",
                        "action": "vehicle modifiée",
                        "error": "vehicle not found"
                    }
                    
                return make_response(jsonify(response_data), 400)

            vehicle.vehicleClass = json_data.get('vehicleClass')
            

            db.session.commit()

            response_data = {
                        "status": "success",
                        "action": "Vehicle modifié",
                        "data": str(vehicle)
                    }
                    
            return make_response(jsonify(response_data), 200)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Vehicle modifié",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)


