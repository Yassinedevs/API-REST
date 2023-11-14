import pymysql
from config import mysql
from flask import jsonify
from flask import flash, request
from flask import Blueprint

routes_planets= Blueprint('planets', __name__)

@routes_planets.route("", methods=["GET"])
def get_all_planets():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name FROM planets")
        planets_rows = cursor.fetchall()
        if planets_rows:
            response_data = {
                "status": "success",
                "message": "Liste de planets récupérée avec succès.",
                "data": planets_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucune planet trouvé.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération de la liste des planets.",
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

@routes_planets.route("<int:id>", methods=["GET"])
def get_one_planet(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name FROM planets WHERE id = %s", (id,))
        planet_rows = cursor.fetchall()

        if planet_rows:
            response_data = {
                "status": "success",
                "message": "planet récupéré avec succès.",
                "data": planet_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucun planet trouvé.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération de la planet.",
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


@routes_planets.route("", methods=["POST"])
def create_one_planet():
    return {"create":"a faire"}


@routes_planets.route("<int:id>", methods=["DELETE"])
def delete_one_planet(id):
    return {"delete":"a faire"}

@routes_planets.route("<int:id>", methods=["PUT"])
def update_one_planet(id):
    return {"update":"a faire"}