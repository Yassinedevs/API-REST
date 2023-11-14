from flask import Flask
from flask_cors import CORS, cross_origin
from routes.routes_films import routes_films
from routes.routes_peoples import routes_peoples
from routes.routes_planets import routes_planets
from routes.routes_species import routes_species
from routes.routes_starships import routes_starships
from routes.routes_vehicles import routes_vehicles
from config import app, mysql

app.register_blueprint(routes_films, url_prefix='/films')
app.register_blueprint(routes_peoples, url_prefix='/peoples')
app.register_blueprint(routes_planets, url_prefix='/planets')
app.register_blueprint(routes_species, url_prefix='/species')
app.register_blueprint(routes_starships, url_prefix='/starships')
app.register_blueprint(routes_vehicles, url_prefix='/vehicules')

# Autres configurations, si nécessaires

if __name__ == "__main__":
    app.run(debug=True)

