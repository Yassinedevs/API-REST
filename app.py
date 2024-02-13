from flask import Flask
from flask_cors import CORS, cross_origin
from routes.routes_films import films_namespace
from routes.routes_peoples import people_namespace
from routes.routes_planets import planets_namespace
from routes.routes_species import species_namespace
from routes.routes_starships import starships_namespace
from routes.routes_vehicles import vehicles_namespace
from flask_restx import Api
from config import app



api = Api(app, version='1.0', title='Votre API', description="""
Bienvenue sur l'API Star Wars, votre passerelle vers l'univers fascinant de la saga intergalactique. Cette API expose des informations détaillées sur les personnages de Star Wars, permettant aux développeurs d'accéder facilement à une mine de données liées à leurs héros préférés.""")
api.add_namespace(films_namespace, path='/films')
api.add_namespace(people_namespace, path='/peoples')
api.add_namespace(planets_namespace, path='/planets')
api.add_namespace(species_namespace, path='/species')
api.add_namespace(starships_namespace, path='/starships')
api.add_namespace(vehicles_namespace, path='/vehicles')

# Autres configurations, si nécessaires

if __name__ == "__main__":
    app.run(debug=True)

