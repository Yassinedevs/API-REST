import pymysql
from config import mysql
from flask import jsonify
from flask import flash, request
from flask import Blueprint

routes_films= Blueprint('films', __name__)

@routes_films.route("", methods=["GET"])
def get_all_films():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, title, producer FROM films")
        film_rows = cursor.fetchall()

        if film_rows:
            response_data = {
                "status": "success",
                "message": "Liste de films récupérée avec succès.",
                "data": film_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucun film trouvé.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération de la liste des films.",
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


@routes_films.route("<int:id>", methods=["GET"])
def get_one_film(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, title, producer FROM films WHERE id = %s", (id,))
        film_rows = cursor.fetchall()

        if film_rows:
            response_data = {
                "status": "success",
                "message": "film récupéré avec succès.",
                "data": film_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucun film trouvé.",
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


@routes_films.route("", methods=["POST"])
def create_one_film():
    return {"create":"a faire"}


@routes_films.route("<int:id>", methods=["DELETE"])
def delete_one_film(id):
    return {"delete":"a faire"}

@routes_films.route("<int:id>", methods=["PUT"])
def update_one_film(id):
    return {"update":"a faire"}