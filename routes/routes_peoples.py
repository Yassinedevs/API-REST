from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace, fields
from models import *
from config import db
from config import BASE_URL
from datetime import datetime
from flask_jwt_extended import jwt_required



people_namespace = Namespace('peoples', description='Endpoints pour les peoples')

people_model = people_namespace.model('PeopleModel', {
    'name': fields.String(required=True, description='Le nom de la personne'),
    'gender': fields.String(description='Le genre de la personne'),
    'skinColor': fields.String(description='La couleur de la peau de la personne'),
    'hairColor': fields.String(description='La couleur des cheveux de la personne'),
    'height': fields.String(description='La taille de la personne'),
    'eyeColor': fields.String(description='La couleur des yeux de la personne'),
    'mass': fields.String(description='La masse de la personne'),
    'birthYear': fields.String(description="L'année de naissance de la personne"),
    'idPlanet': fields.Integer(description="L'ID de la planète associée à la personne"),
    'idStarship': fields.Integer(description="L'ID du vaisseau spatial associé à la personne"),
    'idVehicle': fields.Integer(description="L'ID du véhicule associé à la personne"),
})


@people_namespace.route("")
class PeoplesResource(Resource):
    @jwt_required()
    @people_namespace.doc(security="JsonWebToken")
    def get(self):
        try:
            peoples = People.get_all()
            peoples_list = []
            for people in peoples:
                planet_info = [f"{BASE_URL}/planets/{people.planet.idPlanet}/"]

                starship_info = None
                if people.starship:
                    starship_info = [f"{BASE_URL}/starships/{people.starship.idStarship}/"]

                vehicle_info = None
                if people.vehicle:
                    vehicle_info = [f"{BASE_URL}/vehicles/{people.vehicle.idVehicle}/"]


                peoples_list.append({
                    'url': f"{BASE_URL}/people/{people.idPeople}/",
                    'name': people.name,
                    'gender': people.gender,
                    'skinColor': people.skinColor,
                    'hairColor': people.hairColor,
                    'height': people.height,
                    'eyeColor': people.eyeColor,
                    'mass': people.mass,
                    'birthYear': people.birthYear,
                    'created': people.created.strftime('%Y-%m-%d %H:%M:%S'),
                    'edited': people.edited.strftime('%Y-%m-%d %H:%M:%S'),
                    'planet': planet_info,
                    'starship': starship_info,
                    'vehicle': vehicle_info
                })

            response_data = {
                        "status": "success",
                        "action": "Lister des peoples",
                        "data": peoples_list
                    }
                    
            return make_response(jsonify(response_data), 200)
        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Lister des peoples",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)

    @jwt_required()
    @people_namespace.doc(security="JsonWebToken")
    @people_namespace.expect(people_model, validate=True)
    def post(self):
        try:
            json_data = request.get_json(force=True)

            new_people = People(
                name=json_data.get('name'),
                gender=json_data.get('gender'),
                skinColor=json_data.get('skinColor'),
                hairColor=json_data.get('hairColor'),
                height=json_data.get('height'),
                eyeColor=json_data.get('eyeColor'),
                mass=json_data.get('mass'),
                birthYear=json_data.get('birthYear'),
                created=datetime.now(),
                edited=datetime.now(),
                idPlanet=json_data.get('idPlanet'),
                idStarship=json_data.get('idStarship'),
                idVehicle=json_data.get('idVehicle'),
            )

            db.session.add(new_people)
            db.session.commit()

            response_data = {
                        "status": "success",
                        "action": "People ajouté",
                        "data": new_people
                    }
                    
            return make_response(jsonify(response_data), 200)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "People ajouté",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)




@people_namespace.route("/<int:id>")
class PeopleResource(Resource):
    @jwt_required()
    @people_namespace.doc(security="JsonWebToken")
    def get(self, id):
        try:
            people = People.get_one_by_id(id)
            if people:
                planet_info = {
                    'idPlanet': people.planet.idPlanet,
                    'name': people.planet.name,
                    'climate': people.planet.climate,
                    'surfaceWater': people.planet.surfaceWater,
                    'diameter': people.planet.diameter,
                    'rotationPeriod': people.planet.rotationPeriod,
                    'created': people.planet.created.strftime('%Y-%m-%d %H:%M:%S'),
                    'terrain': people.planet.terrain,
                    'gravity': people.planet.gravity,
                    'orbitalPeriod': people.planet.orbitalPeriod,
                    'population': people.planet.population
                }

                starship_info = None
                if people.starship:
                    starship_info = {
                        'idStarship': people.starship.idStarship,
                        'MGLT': people.starship.MGLT,
                        'starshipClass': people.starship.starshipClass,
                        'hyperdriveRating': people.starship.hyperdriveRating
                    }

                vehicle_info = None
                if people.vehicle:
                    vehicle_info = {
                        'idVehicle': people.vehicle.idVehicle,
                        'vehicleClass': people.vehicle.vehicleClass
                    }

                people_data = {
                    'idPeople': people.idPeople,
                    'name': people.name,
                    'gender': people.gender,
                    'skinColor': people.skinColor,
                    'hairColor': people.hairColor,
                    'height': people.height,
                    'eyeColor': people.eyeColor,
                    'mass': people.mass,
                    'birthYear': people.birthYear,
                    'created': people.created.strftime('%Y-%m-%d %H:%M:%S'),
                    'edited': people.edited.strftime('%Y-%m-%d %H:%M:%S'),
                    'planet': planet_info,
                    'starship': starship_info,
                    'vehicle': vehicle_info
                }

            response_data = {
                        "status": "success",
                        "action": "Récupéré un people",
                        "data": people_data
                    }
                    
            return make_response(jsonify(response_data), 200)
        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Récupérer un people",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)

    @jwt_required()
    @people_namespace.doc(security="JsonWebToken")
    def delete(self, id):
        try:
            existing_people = People.get_one_by_id(id)

            if existing_people:
                # Supprimer d'abord les enregistrements liés dans les tables de jonction
                FilmsPeople.query.filter(FilmsPeople.idPeople == id).delete()
                PeopleSpecies.query.filter(PeopleSpecies.idPeople == id).delete()
                # Vous pouvez répéter cette opération pour d'autres tables de jonction si nécessaire

                # Ensuite, supprimer l'entrée principale dans la table people
                db.session.delete(existing_people)
                db.session.commit()

                response_data = {
                    "status": "success",
                    "action": "People supprimé",
                    "data": existing_people
                }

                return make_response(jsonify(response_data), 200)
            else:
                response_data = {
                    "status": "error",
                    "action": "People supprimé",
                    "error": "People non trouvé"
                }

                return make_response(jsonify(response_data), 400)

        except Exception as e:
            response_data = {
                "status": "error",
                "action": "People supprimé",
                "error": str(e)
            }

            return make_response(jsonify(response_data), 400)
        
    @jwt_required()
    @people_namespace.doc(security="JsonWebToken")
    @people_namespace.expect(people_model, validate=True)
    def post(self, id):
        try:
            json_data = request.get_json(force=True)
            
            existing_people = People.get_one_by_id(id)

            if existing_people:
                existing_people.name = json_data.get('name', existing_people.name)
                existing_people.gender = json_data.get('gender', existing_people.gender)
                existing_people.skinColor = json_data.get('skinColor', existing_people.skinColor)
                existing_people.hairColor = json_data.get('hairColor', existing_people.hairColor)
                existing_people.height = json_data.get('height', existing_people.height)
                existing_people.eyeColor = json_data.get('eyeColor', existing_people.eyeColor)
                existing_people.mass = json_data.get('mass', existing_people.mass)
                existing_people.birthYear = json_data.get('birthYear', existing_people.birthYear)
                existing_people.edited = datetime.now()

                existing_people.idPlanet = json_data.get('idPlanet', existing_people.idPlanet)
                existing_people.idStarship = json_data.get('idStarship', existing_people.idStarship)
                existing_people.idVehicle = json_data.get('idVehicle', existing_people.idVehicle)

                db.session.commit()

                response_data = {
                        "status": "success",
                        "action": "Film modifié",
                        "data": existing_people
                    }
                    
                return make_response(jsonify(response_data), 200)
            else:
                response_data = {
                        "status": "error",
                        "actcion": "People modifié",
                        "error": "People not found"
                    }
                    
                return make_response(jsonify(response_data), 400)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "People modifié",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)


