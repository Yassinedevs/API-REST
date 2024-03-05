from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace, fields
from models import *
from config import db
from config import BASE_URL
from flask_jwt_extended import jwt_required
from datetime import datetime

species_namespace = Namespace('species', description='Endpoints pour les species')

species_model = species_namespace.model('Species', {
    'name': fields.String(required=True, description='Nom de la specie'),
    'classification': fields.String(required=True, description='Classification de la specie'),
    'designation': fields.String(required=True, description='Designation de la specie'),
    'eyeColors': fields.String(required=True, description='Couleur de la specie'),
    'skinColors': fields.String(required=True, description='skinColors de la specie'),
    'language': fields.String(required=True, description='language de la specie'),
    'averageLifespan': fields.String(required=True, description='averageLifespan de la specie'),
    'averageHeight': fields.String(required=True, description='averageHeight de la specie'),
    'planet': fields.Integer(required=True, description='planet de la specie'),
})


@species_namespace.route("")
class PlanetsResource(Resource):
    @jwt_required()
    @species_namespace.doc(security="JsonWebToken")    
    def get(self):
        try:
            species = Species.get_all()
            species_list = []
            for specie in species:
                planet = specie.planet
                if planet == None: 
                    planet_list = ""
                else:
                    planet_list = f"{BASE_URL}/planets/{planet.idPlanet}/"
                
                species_list.append({
                    'idSpecie': specie.idSpecie,
                    'classification': specie.classification,
                    'name': specie.name,
                    'designation': specie.designation,
                    'eyeColors': specie.eyeColors,
                    'people': specie.people,
                    'skinColors': specie.skinColors,
                    'language': specie.language,
                    'hairColors': specie.hairColors,
                    'averageLifespan': specie.averageLifespan,
                    'averageHeight': specie.averageHeight,
                    'planet': planet_list,
                    'created': specie.created.strftime('%Y-%m-%d %H:%M:%S'),
                    'edited': specie.edited.strftime('%Y-%m-%d %H:%M:%S')
                })

                response_data = {
                        "status": "success",
                        "action": "Species listées",
                        "data": species_list
                    }
                    
            return make_response(jsonify(response_data), 200)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Species listées",
                        "data": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)
    
    @jwt_required()
    @species_namespace.doc(security="JsonWebToken") 
    @species_namespace.expect(species_model)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            new_specie = Species(
                name=json_data.get('name'),
                classification=json_data.get('classification'),
                designation=json_data.get('designation'),
                eyeColors=json_data.get('eyeColors'),
                skinColors=json_data.get('skinColors'),
                language=json_data.get('language'),
                averageLifespan=json_data.get('averageLifespan'),
                averageHeight=json_data.get('averageHeight'),
                created=datetime.now(),
                edited=datetime.now(),
                idPlanet = json_data.get('planet')
            )

            db.session.add(new_specie)
            db.session.commit()

            response_data = {
                        "status": "success",
                        "action": "Specie ajoutée",
                        "data": str(new_specie)
                    }
                    
            return make_response(jsonify(response_data), 200)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Specie ajoutée",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)


@species_namespace.route("/<int:id>")
class PlanetResource(Resource):
    @jwt_required()
    @species_namespace.doc(security="JsonWebToken") 
    def get(self, id):
        try:
            specie = Species.get_one_by_id(id)
            if specie:
                planet = specie.planet
                if planet == None: 
                    planet_list = ""
                else:
                    planet_list = f"{BASE_URL}/planets/{planet.idPlanet}/"
                specie_data = {
                    'idSpecie': specie.idSpecie,
                    'classification': specie.classification,
                    'name': specie.name,
                    'designation': specie.designation,
                    'eyeColors': specie.eyeColors,
                    'people': specie.people,
                    'skinColors': specie.skinColors,
                    'language': specie.language,
                    'hairColors': specie.hairColors,
                    'averageLifespan': specie.averageLifespan,
                    'averageHeight': specie.averageHeight,
                    'planet': planet_list,
                    'created': specie.created.strftime('%Y-%m-%d %H:%M:%S'),
                    'edited': specie.edited.strftime('%Y-%m-%d %H:%M:%S')
                }

                response_data = {
                    "status": "success",
                    "action": "Lister un specie",
                    "data": specie_data
                }
                
                return make_response(jsonify(response_data), 200)
            else:
                response_data = {
                    "status": "error",
                    "action": "Lister un specie",
                    "error": "Specie not found"
                }
                return make_response(jsonify(response_data), 400)


        except Exception as e:
            response_data = {
                    "status": "error",
                    "action": "Lister un specie",
                    "error": str(e)
                }
            return make_response(jsonify(response_data), 400)
    
    @jwt_required()
    @species_namespace.doc(security="JsonWebToken") 
    def delete(self, id):
        try:
            existing_specie = Species.get_one_by_id(id)

            if existing_specie:
                db.session.delete(existing_specie)
                db.session.commit()

                response_data = {
                        "status": "success",
                        "action": "Specie supprimée",
                        "data": str(existing_specie)
                    }
                    
                return make_response(jsonify(response_data), 200)
            else:
                response_data = {
                        "status": "error",
                        "action": "Specie supprimée",
                        "error": "Specie not found"
                    }
                    
                return make_response(jsonify(response_data), 400)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Specie supprimé",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)
    
    @jwt_required()
    @species_namespace.doc(security="JsonWebToken") 
    @species_namespace.expect(species_model)
    def post(self, id):
        try:
            json_data = request.get_json(force=True)
            specie = Species.get_one_by_id(id)

            if not specie:
                response_data = {
                        "status": "error",
                        "action":"Modifier une specie",
                        "error": "Specie non trouvée",
                    }
                    
                return make_response(jsonify(response_data), 400)

            specie.name=json_data.get('name')
            specie.edited=datetime.now()
            specie.classification=json_data.get('classification')
            specie.eyeColors=json_data.get('eyeColors')
            specie.skinColors=json_data.get('skinColors')
            specie.language=json_data.get('language')
            specie.hairColors=json_data.get('hairColors')
            specie.averageLifespan=json_data.get('averageLifespan')
            specie.averageHeight=json_data.get('averageHeight')
            specie.planet=json_data.get('idPlanet')
            
            db.session.commit()


            response_data = {
                        "status": "success",
                        "action": "Specie modifiée",
                        "data": str(specie)
                    }
                    
            return make_response(jsonify(response_data), 200)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action":"Modifier une Specie",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)


