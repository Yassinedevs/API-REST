import pymysql
from config import mysql
from flask import jsonify
from flask import flash, request
from flask import Blueprint

routes_species= Blueprint('species', __name__)

@routes_species.route("", methods=["GET"])
def get_all_species():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id,classification, name FROM species")
        species_rows = cursor.fetchall()
        if species_rows:
            response_data = {
                "status": "success",
                "message": "Liste de species récupérée avec succès.",
                "data": species_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucune specie trouvé.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération de la liste des species.",
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

@routes_species.route("<int:id>", methods=["GET"])
def get_one_specie(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id,classification, name FROM species WHERE id = %s", (id,))
        specie_rows = cursor.fetchall()

        if specie_rows:
            response_data = {
                "status": "success",
                "message": "specie récupérée avec succès.",
                "data": specie_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucune specie trouvée.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération de la specie.",
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


@routes_species.route("", methods=["POST"])
def create_one_specie():
    return {"create":"a faire"}


@routes_species.route("<int:id>", methods=["DELETE"])
def delete_one_specie(id):
    return {"delete":"a faire"}

@routes_species.route("<int:id>", methods=["PUT"])
def update_one_specie(id):
    return {"update":"a faire"}