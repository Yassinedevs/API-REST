import pymysql
from config import mysql
from flask import jsonify
from flask import flash, request
from flask import Blueprint

routes_peoples= Blueprint('peoples', __name__)

@routes_peoples.route("", methods=["GET"])
def get_all_peoples():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name FROM people")
        
        peoples_rows = cursor.fetchall()
        if peoples_rows:
            response_data = {
                "status": "success",
                "message": "Liste de peoples récupérée avec succès.",
                "data": peoples_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucun people trouvé.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération de la liste des peoples.",
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

@routes_peoples.route("<int:id>", methods=["GET"])
def get_one_people(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name FROM people WHERE id = %s", (id,))
        people_rows = cursor.fetchall()

        if people_rows:
            response_data = {
                "status": "success",
                "message": "people récupéré avec succès.",
                "data": people_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucun people trouvé.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération du people.",
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


@routes_peoples.route("", methods=["POST"])
def create_one_people():
    return {"create":"a faire"}


@routes_peoples.route("<int:id>", methods=["DELETE"])
def delete_one_people(id):
    return {"delete":"a faire"}

@routes_peoples.route("<int:id>", methods=["PUT"])
def update_one_people(id):
    return {"update":"a faire"}