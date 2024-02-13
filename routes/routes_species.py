from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from models import *
from config import db


species_namespace = Namespace('species', description='Endpoints pour les species')


@species_namespace.route("")
class PlanetsResource(Resource):
    def get(self):
        try:
            species = Species.get_all()
            species_list = []
            for specie in species:
                
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
                    'created': specie.created.strftime('%Y-%m-%d %H:%M:%S'),
                    'edited': specie.edited.strftime('%Y-%m-%d %H:%M:%S')

                })

            return jsonify({'species': species_list})
        except Exception as e:
            return jsonify({'error': str(e)})

    def post(self):
        return {"create":"a faire"}


@species_namespace.route("/<int:id>")
class PlanetResource(Resource):
    def get(self, id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT name FROM species WHERE id = %s", (id,))
            film_rows = cursor.fetchall()

            if film_rows:
                response_data = {
                    "status": "success",
                    "message": "species récupéré avec succès.",
                    "data": film_rows
                }
                status_code = 200
            else:
                response_data = {
                    "status": "success",
                    "message": "Aucun species trouvé.",
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


