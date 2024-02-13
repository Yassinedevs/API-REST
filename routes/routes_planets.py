from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from models import *
from config import db
from datetime import datetime
import json
from flask_jwt_extended import jwt_required

planets_namespace = Namespace('planets', description='Endpoints pour les peoples')

planet_model = planets_namespace.model('Planet', {
    'name': fields.String(required=True, description='Nom de la planète'),
    'climate': fields.String(required=True, description='Climat de la planète'),
    'surfaceWater': fields.String(required=True, description='Surface d\'eau de la planète'),
    'diameter': fields.Integer(required=True, description='Diamètre de la planète'),
    'rotationPeriod': fields.Integer(required=True, description='Période de rotation de la planète'),
    'terrain': fields.String(required=True, description='Type de terrain de la planète'),
    'gravity': fields.String(required=True, description='Gravité de la planète'),
    'orbitalPeriod': fields.Integer(required=True, description='Période orbitale de la planète'),
    'population': fields.Integer(required=True, description='Population de la planète'),
})

@planets_namespace.route("")
class PlanetsResource(Resource):
    @jwt_required()
    @planets_namespace.doc(security="JsonWebToken")
    def get(self):
        try:
            planets = Planets.get_all()
            planets_list = []
            for planet in planets:
                planets_list.append({
                    'idPlanet': planet.idPlanet,
                    'name': planet.name,
                    'climate': planet.climate,
                    'surfaceWater': planet.surfaceWater,
                    'diameter': planet.diameter,
                    'rotationPeriod': planet.rotationPeriod,
                    'created': planet.created.strftime('%Y-%m-%d %H:%M:%S'),
                    'terrain': planet.terrain,
                    'gravity': planet.gravity,
                    'orbitalPeriod': planet.orbitalPeriod,
                    'population': planet.population,
                })

            response_data = {
                        "status": "success",
                        "action": "Planets listées",
                        "data": planets_list
                    }
                    
            return jsonify(response_data)
        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Planets listées",
                        "error": str(e)
                    }
                    
            return jsonify(response_data)

    @jwt_required()
    @planets_namespace.doc(security="JsonWebToken")
    @planets_namespace.expect(planet_model)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            new_planet = Planets(
                name=json_data.get('name'),
                climate=json_data.get('climate'),
                surfaceWater=json_data.get('surfaceWater'),
                diameter=json_data.get('diameter'),
                rotationPeriod=json_data.get('rotationPeriod'),
                terrain=json_data.get('terrain'),
                gravity=json_data.get('gravity'),
                orbitalPeriod=json_data.get('orbitalPeriod'),
                population=json_data.get('population'),
                created=datetime.now()
            )

            db.session.add(new_planet)
            db.session.commit()

            response_data = {
                        "status": "error",
                        "action": "Planet ajoutée",
                        "data": new_planet
                    }
                    
            return jsonify(response_data)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Planet ajoutée",
                        "error": str(e)
                    }
                    
            return jsonify(response_data)

@planets_namespace.route("/<int:id>")
class PlanetResource(Resource):
    @jwt_required()
    @planets_namespace.doc(security="JsonWebToken")
    def get(self, id):
        try:
            planet = Planets.get_one_by_id(id)
            if planet:
                planet_data = {
                    'idPlanet': planet.idPlanet,
                    'name': planet.name,
                    'climate': planet.climate,
                    'surfaceWater': planet.surfaceWater,
                    'diameter': planet.diameter,
                    'rotationPeriod': planet.rotationPeriod,
                    'created': planet.created.strftime('%Y-%m-%d %H:%M:%S'),
                    'terrain': planet.terrain,
                    'gravity': planet.gravity,
                    'orbitalPeriod': planet.orbitalPeriod,
                    'population': planet.population,
                }

                response_data = {
                    "status": "success",
                    "action": "planet listée",
                    "data": planet_data
                }

                return jsonify(response_data)
            else:
                response_data = {
                            "status": "error",
                            "action": "Planet listée",
                            "error": "Planet not found"
                        }
                        
                return jsonify(response_data)
        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Planet listée",
                        "error": str(e)
                    }
                    
            return jsonify(response_data)
    
    @jwt_required()
    @planets_namespace.doc(security="JsonWebToken")
    def delete(self, id):
        try:
            planet_to_delete = Planets.get_one_by_id(id)

            # Vérifiez si la planète a été trouvée
            if planet_to_delete:
                # Marquez la planète à supprimer
                db.session.delete(planet_to_delete)

                # Effectuez un commit pour appliquer la suppression dans la base de données
                db.session.commit()

                response_data = {
                        "status": "success",
                        "action": "Planet supprimé",
                        "data": planet_to_delete
                    }
                    
                return jsonify(response_data)
            else:
                response_data = {
                        "status": "error",
                        "action": "Planet supprimée",
                        "error": "Planet not found"
                    }
                    
                return jsonify(response_data)
        
        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Planet suprimée",
                        "error": str(e)
                    }
                    
            return jsonify(response_data)
    
    @jwt_required()
    @planets_namespace.doc(security="JsonWebToken")
    @planets_namespace.expect(planet_model)
    def post(self, id):
        try:
            json_data = request.get_json(force=True)
            planet = Planets.get_one_by_id(id)

            if not planet:
                response_data = {
                        "status": "error",
                        "action": "Planet modifiée",
                        "error": "Planet not found"
                    }
                    
                return jsonify(response_data)

            planet.name = json_data.get('name')
            planet.climate = json_data.get('climate')
            planet.surfaceWater = json_data.get('surfaceWater')
            planet.diameter = json_data.get('diameter')
            planet.rotationPeriod = json_data.get('rotationPeriod')
            planet.terrain = json_data.get('terrain')
            planet.gravity = json_data.get('gravity')
            planet.orbitalPeriod = json_data.get('orbitalPeriod')
            planet.population = json_data.get('population')

            db.session.commit()

            response_data = {
                        "status": "success",
                        "action": "Planet modifiée",
                        "data": planet
                    }
                    
            return jsonify(response_data)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Planet modifiée",
                        "error": str(e)
                    }
                    
            return jsonify(response_data)
