from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from models import *
from config import db
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

            return jsonify({'starships': starships_list})
        except Exception as e:
            return jsonify({'error': str(e)})
    
    @jwt_required()
    @starships_namespace.doc(security="JsonWebToken") 
    def post(self):
        return {"create":"a faire"}


@starships_namespace.route("/<int:id>")
class StarshipResource(Resource):
    @jwt_required()
    @starships_namespace.doc(security="JsonWebToken") 
    def get(self, id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = '''
                    SELECT t.name, t.model, t.manufacturer, t.costInCredits, t.length, t.maxAtmospheringSpeed, t.crew, t.passengers, t.cargoCapacity, t.consumables, s.hyperdriveRating, s.MGLT, s.starshipClass, p.idPeople as "pilots", fs.idFilm as "films", t.created, t.edited, s.idStarship as "url"
                    FROM starships s
                    LEFT JOIN transport t ON s.idTransport = t.idTransport
                    LEFT JOIN filmsstarships fs ON s.idStarship = fs.idStarship
                    LEFT JOIN people p ON s.idStarship = p.idStarship
                    WHERE s.idStarship = %s;
                '''
            cursor.execute(query, (id,))
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
    
    @jwt_required()
    @starships_namespace.doc(security="JsonWebToken") 
    def delete(self, id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM starships WHERE idStarship = %s", (id,))
            film_rows = cursor.fetchall()

            if film_rows :
                cursor = conn.cursor()
                cursor.execute("DELETE FROM filmsstarships WHERE idStarship = %s", (id,))
                cursor.execute("DELETE FROM starships WHERE idStarship = %s", (id,))
                response_data = {
                    "status": "success",
                    "message": "starships supprimé avec succès.",
                    "data": film_rows
                }
                status_code = 200
            else :
                response_data = {
                    "status": "error",
                    "message": "Aucun starships trouvé.",
                    "data": []
                }
                status_code = 404

        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Échec de la suppression du starship.",
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

    @jwt_required()
    @starships_namespace.doc(security="JsonWebToken") 
    @starships_namespace.expect(starship_model)
    def put(self, id):
        try :
            conn = mysql.connect()
            cursor = conn.cursor()
            query = '''
                    UPDATE starships
                    SET MGLT = %s, starshipClass = %s, hyperdriveRating = %s, idTransport = %s
                    WHERE idStarship = %s
                '''
 
            values = (
                json_data.get('MGLT'),
                json_data.get('starshipClass'),
                json_data.get('hyperdriveRating'),
                json_data.get('idTransport'),
                id
            )

            cursor.execute(query, values)

        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Échec de la suppression du starship.",
                "error_code": "INTERNAL_SERVER_ERROR",
                "details": str(e)
            }
            status_code = 500
        finally:
            cursor.close() 
            conn.close()  

 
            return {'message': 'Mise à jour du vaisseau avec succès'}