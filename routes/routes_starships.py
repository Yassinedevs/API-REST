from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from models import *
from config import db


starships_namespace = Namespace('starships', description='Endpoints pour les starships')


@starships_namespace.route("")
class StarshipsResource(Resource):
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

            return jsonify({'starships': starships_list})
        except Exception as e:
            return jsonify({'error': str(e)})

    def post(self):
        return {"create":"a faire"}


@starships_namespace.route("/<int:id>")
class StarshipResource(Resource):
    def get(self, id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT starship_class FROM starships WHERE id = %s", (id,))
            film_rows = cursor.fetchall()

            if film_rows:
                response_data = {
                    "status": "success",
                    "message": "starships récupéré avec succès.",
                    "data": film_rows
                }
                status_code = 200
            else:
                response_data = {
                    "status": "success",
                    "message": "Aucun starships trouvé.",
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


