import pymysql
from config import mysql
from flask import jsonify
from flask import flash, request
from flask import Blueprint

routes_starships= Blueprint('starships', __name__)

@routes_starships.route("", methods=["GET"])
def get_all_starships():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, starship_class FROM starships")
        starships_rows = cursor.fetchall()
        if starships_rows:
            response_data = {
                "status": "success",
                "message": "Liste de starships récupérée avec succès.",
                "data": starships_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucune starship trouvé.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération de la liste des starships.",
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

@routes_starships.route("<int:id>", methods=["GET"])
def get_one_starship(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, starship_class FROM starships WHERE id = %s", (id,))
        starship_rows = cursor.fetchall()

        if starship_rows:
            response_data = {
                "status": "success",
                "message": "starship récupérée avec succès.",
                "data": starship_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucune starship trouvée.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération de la starship.",
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


@routes_starships.route("", methods=["POST"])
def create_one_starship():
    return {"create":"a faire"}


@routes_starships.route("<int:id>", methods=["DELETE"])
def delete_one_starship(id):
    return {"delete":"a faire"}

@routes_starships.route("<int:id>", methods=["PUT"])
def update_one_starship(id):
    return {"update":"a faire"}