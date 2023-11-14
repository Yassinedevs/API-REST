from flask import Flask
from flask_cors import CORS, cross_origin
from routes.routes_films import routes_films
from config import app, mysql

app.register_blueprint(routes_films, url_prefix='/films')

# Autres configurations, si nécessaires

if __name__ == "__main__":
    app.run(debug=True)

