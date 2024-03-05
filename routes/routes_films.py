from flask import jsonify, request, url_for, make_response
from flask_restx import Resource, Namespace, fields
from models import *
from config import db
from config import BASE_URL
from datetime import datetime
import json
from flask_jwt_extended import jwt_required



films_namespace = Namespace('films', description='Endpoints pour les films')
film_model = films_namespace.model('FilmModel', {
    'producer': fields.String(description='Producteur du film'),
    'title': fields.String(required=True, description='Titre du film'),
    'episodeId': fields.Integer(description="ID de l'épisode"),
    'director': fields.String(description='Réalisateur du film'),
    'releaseDate': fields.Date(description='Date de sortie du film'),
    'openingCrawl': fields.String(description='Introduction du film'),
    'peoples': fields.List(fields.Integer(description='ID de la personne')),
    'planets': fields.List(fields.Integer(description='ID de la planète')),
    'species': fields.List(fields.Integer(description='ID de l\'espèce')),
    'starships': fields.List(fields.Integer(description='ID du vaisseau spatial')),
})

@films_namespace.route("")
class FilmsResource(Resource):
    @jwt_required()
    @films_namespace.doc(security="JsonWebToken")
    def get(self):
        try:
            films = Films.get_all()
            films_list = []

            for film in films:
                species_list = [f"{BASE_URL}/species/{fs.specie.idSpecie}/" for fs in film.species]
                starships_list = [f"{BASE_URL}/starships/{fs.starship.idStarship}/" for fs in film.films_starships]
                people_list = [f"{BASE_URL}/peoples/{fp.people.idPeople}/" for fp in film.films_people]
                planets_list = [f"{BASE_URL}/planets/{fp.planet.idPlanet}/" for fp in film.films_planets]


                films_list.append({
                    'idFilm': film.idFilm,
                    'producer': film.producer,
                    'title': film.title,
                    'episodeId': film.episodeId,
                    'director': film.director,
                    'releaseDate': film.releaseDate.strftime('%Y-%m-%d'),
                    'openingCrawl': film.openingCrawl,
                    'species': species_list,
                    'starships': starships_list,
                    'peoples': people_list,
                    'planets': planets_list,
                })
                
            response_data = {
                        "status": "success",
                        "action": "Lister les films",
                        "data": films_list
                    }
                    
            return make_response(jsonify(response_data), 200)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Lister les films",
                        "error": str(e),
                    }
                    
            return make_response(jsonify(response_data), 400)

    @jwt_required()
    @films_namespace.doc(security="JsonWebToken")
    @films_namespace.expect(film_model)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            new_film = Films(
                title=json_data.get('title'),
                edited=datetime.now(),
                created=datetime.now(),
                producer=json_data.get('producer'),
                episodeId=json_data.get('episodeId'),
                director=json_data.get('director'),
                releaseDate=json_data.get('releaseDate'),
                openingCrawl=json_data.get('openingCrawl'),

            )
            db.session.add(new_film)
            db.session.commit()
            for specie_id in json_data.get("species"):
                film_species = FilmsSpecies(idFilm=new_film.idFilm, idSpecie=specie_id)
                db.session.add(film_species)
            
            for people_id in json_data.get("people"):
                film_people = FilmsPeople(idFilm=new_film.idFilm, idPeople=people_id)
                db.session.add(film_people)
            
            for starship_id in json_data.get("starships"):
                starship_people = FilmsStarships(idFilm=new_film.idFilm, idStarship=starship_id)
                db.session.add(starship_people)
            
            for planet_id in json_data.get("planets"):
                planet_people = FilmsPlanets(idFilm=new_film.idFilm, idPlanet=planet_id)
                db.session.add(planet_people)

            # Effectuez un autre commit pour enregistrer les modifications de relation dans la base de données
            db.session.commit()

            response_data = {
                        "status": "success",
                        "action": "Ajouter un film",
                        "data": new_film
                    }
                    
            return make_response(jsonify(response_data), 200)
        
        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Ajouter un film",
                        "error": str(e),
                    }
                    
            return make_response(jsonify(response_data), 400)



@films_namespace.route("/<int:id>")
class FilmResource(Resource):
    @jwt_required()
    @films_namespace.doc(security="JsonWebToken")
    def get(self, id):
            try:
                film = Films.get_one_by_id(id)
                if film:
                    film_data = {
                        'idFilm': film.idFilm,
                        'edited': film.edited.strftime('%Y-%m-%d %H:%M:%S'),
                        'producer': film.producer,
                        'title': film.title,
                        'created': film.created.strftime('%Y-%m-%d %H:%M:%S'),
                        'episodeId': film.episodeId,
                        'director': film.director,
                        'releaseDate': film.releaseDate.strftime('%Y-%m-%d'),
                        'openingCrawl': film.openingCrawl
                    }

                    response_data = {
                        "status": "success",
                        "action": "Lister les films",
                        "data": film_data
                    }
                    
                    return make_response(jsonify(response_data), 200)
                else:
                    response_data = {
                        "status": "error",
                        "action": "Lister les films",
                        "error": "Film not found"
                    }
                    return make_response(jsonify(response_data), 400)
    

            except Exception as e:
                response_data = {
                        "status": "error",
                        "action": "Lister les films",
                        "error": str(e)
                    }
                return make_response(jsonify(response_data), 400)
    
    @jwt_required()
    @films_namespace.doc(security="JsonWebToken")
    def delete(self, id):
        try:
            existing_film = Films.get_one_by_id(id)

            if existing_film:
                db.session.delete(existing_film)
                db.session.commit()

                response_data = {
                        "status": "success",
                        "action": "Film supprimé",
                        "data": existing_film
                    }
                    
                return make_response(jsonify(response_data), 200)
            else:
                response_data = {
                        "status": "error",
                        "action": "Film supprimé",
                        "error": "Film not found"
                    }
                    
                return make_response(jsonify(response_data), 400)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action": "Film supprimé",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 400)

    @jwt_required()
    @films_namespace.doc(security="JsonWebToken")
    @films_namespace.expect(film_model)
    def post(self, id):
        try:
            json_data = request.get_json(force=True)
            film = Films.get_one_by_id(id)

            if not film:
                response_data = {
                        "status": "error",
                        "action":"Modifier un film",
                        "error": "Film non trouvé",
                    }
                    
                return make_response(jsonify(response_data), 400)

            film.title=json_data.get('title'),
            film.edited=datetime.now(),
            film.producer=json_data.get('producer'),
            film.episodeId=json_data.get('episodeId'),
            film.director=json_data.get('director'),
            film.releaseDate=json_data.get('releaseDate'),
            film.openingCrawl=json_data.get('openingCrawl'),

            db.session.commit()


            response_data = {
                        "status": "success",
                        "action": "Film modifié",
                        "data": film
                    }
                    
            return make_response(jsonify(response_data), 200)

        except Exception as e:
            response_data = {
                        "status": "error",
                        "action":"Modifier un film",
                        "error": str(e)
                    }
                    
            return make_response(jsonify(response_data), 200)


