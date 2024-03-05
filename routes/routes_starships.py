from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace, fields
from models import *
from config import db
from config import BASE_URL
from datetime import datetime
import json
from flask_jwt_extended import jwt_required

starships_namespace = Namespace('starships', description='Endpoints pour les starships')
starship_model = starships_namespace.model('StarshipModel', {
    'MGLT': fields.String(required=True, description='La vitesse Megalumière par heure'),
    'starshipClass': fields.String(description='Le type de vaisseau'),
    'hyperdriveRating': fields.String(description='Catégorie de vitesse'),
    'idTransport': fields.String(description="L'ID technique du vaisseau"),
})


@starships_namespace.route("")
class StarshipsResource(Resource):
    @jwt_required()
    @starships_namespace.doc(security="JsonWebToken") 
    def get(self):
        try:
            starships = Starships.get_all()
            starships_list = []
            for starship in starships:
                
                starships_list.append({
                    'idStarship': starship.idStarship,
                    'MGLT': starship.MGLT,
                    'starshipClass': starship.starshipClass,
                    'hyperdriveRating': starship.hyperdriveRating,
                    
                })

            response_data = {
                        "status": "success",
                        "action": "Lister les starships",
                        "data": starships_list
                    }

            return jsonify(response_data)
        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Lister les starships",
                        "error": str(e),
                    }
                    
            return jsonify(response_data)
    
    @jwt_required()
    @starships_namespace.doc(security="JsonWebToken") 
    def post(self):
        try:
            json_data = request.get_json(force=True)
            new_starship = Starships(
                MGLT=json_data.get('MGLT'),
                starshipClass=json_data.get('starshipClass'),
                hyperdriveRating=json_data.get('hyperdriveRating'),
                idTransport=json_data.get('idTransport'),
            )
            db.session.add(new_starship)
            db.session.commit()

            response_data = {
                        "status": "success",
                        "action": "Ajouter un starship",
                        "data": new_starship
                    }
                    
            return jsonify(response_data)
        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Ajouter un starship",
                        "error": str(e),
                    }
                    
            return jsonify(response_data)


@starships_namespace.route("/<int:id>")
class StarshipResource(Resource):
    @jwt_required()
    @starships_namespace.doc(security="JsonWebToken") 
    def get(self, id):
        try:
            starship = Starships.get_one_by_id(id)
            transport = Transport.get_one_by_id(id)
            if starship:
                starship_data = {
                    'name': transport.name,
                    'model': transport.model,
                    'manufacturer': transport.manufacturer,
                    'costInCredits': transport.costInCredits,
                    'length': transport.length,
                    'maxAtmospheringSpeed': transport.maxAtmospheringSpeed,
                    'crew': transport.crew,
                    'passengers': transport.passengers,
                    'cargoCapacity': transport.cargoCapacity,
                    'consumables': transport.consumables,
                    'hyperdriveRating': starship.hyperdriveRating,
                    'MGLT': starship.MGLT,
                    'starshipClass': starship.starshipClass,
                    'created': transport.created.strftime('%Y-%m-%d %H:%M:%S'),
                    'edited': transport.edited.strftime('%Y-%m-%d %H:%M:%S'),
                    'idStarship': starship.idStarship
                }

                response_data = {
                        "status": "success",
                        "message": "starships récupéré avec succès.",
                        "data": starship_data
                    }
                status_code = 200
                return make_response(jsonify(response_data), 200)
            else:
                    response_data = {
                        "status": "success",
                        "message": "Aucun starships trouvé.",
                        "data": []
                    }
                    status_code = 200
                    return make_response(jsonify(response_data), 200)
        
        except Exception as e:
                response_data = {
                    "status": "error",
                    "message": "Échec de la récupération du starship.",
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "details": str(e)
                }
                status_code = 500
                return make_response(jsonify(response_data), 500)
    
    @jwt_required()
    @starships_namespace.doc(security="JsonWebToken") 
    def delete(self, id):
        try:
            starship_to_delete = Starships.get_one_by_id(id)

            if starship_to_delete :
                FilmsStarships.query.filter(FilmsStarships.idStarship==id).delete()
                db.session.delete(starship_to_delete)
                db.session.commit()

                response_data = {
                        "status": "success",
                        "action": "Starship supprimé"
                    }
                    
                return make_response(jsonify(response_data), 200)
            else :
                response_data = {
                        "status": "error",
                        "action": "Starship supprimée",
                        "error": "Starship not found"
                    }
                return make_response(jsonify(response_data), 404)

        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Échec de la suppression du starship.",
                "error_code": "INTERNAL_SERVER_ERROR",
                "details": str(e)
            }
            return make_response(jsonify(response_data), 500)

    @jwt_required()
    @starships_namespace.doc(security="JsonWebToken") 
    @starships_namespace.expect(starship_model)
    def put(self, id):
        try :
            json_data = request.get_json(force=True)
            starship = Starships.get_one_by_id(id)
            transport = Transport.get_one_by_id(id)

            if not starship:
                response_data = {
                        "status": "error",
                        "action": "Starship modifiée",
                        "error": "Starship not found"
                    }
                    
                return make_response(jsonify(response_data), 200)
 
            transport.name = json_data.get('name')
            transport.model = json_data.get('model')
            transport.manufacturer = json_data.get('manufacturer')
            transport.costInCredits = json_data.get('costInCredits')
            transport.length = json_data.get('length')
            transport.maxAtmospheringSpeed = json_data.get('maxAtmospheringSpeed')
            transport.crew = json_data.get('crew')
            transport.passengers = json_data.get('passengers')
            transport.cargoCapacity = json_data.get('cargoCapacity')
            transport.consumables = json_data.get('consumables')
            starship.hyperdriveRating = json_data.get('hyperdriveRating')
            starship.MGLT = json_data.get('MGLT')
            starship.starshipClass = json_data.get('starshipClass')
            transport.created = json_data.get('created')
            transport.edited = json_data.get('edited')

            db.session.commit()

            response_data = {
                        "status": "success",
                        "action": "Starship modifiée",
                        "data": [starship, transport]
                    }
            
            return make_response(jsonify(response_data), 200)

        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Échec de la suppression du starship.",
                "error_code": "INTERNAL_SERVER_ERROR",
                "details": str(e)
            }
            return make_response(jsonify(response_data), 500)