import pymysql
from config import mysql
from flask import jsonify
from flask import flash, request
from flask import Blueprint

routes_vehicles= Blueprint('vehicles', __name__)

@routes_vehicles.route("", methods=["GET"])
def get_all_vehicles():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, vehicle_class FROM vehicles")
        vehicles_rows = cursor.fetchall()
        if vehicles_rows:
            response_data = {
                "status": "success",
                "message": "Liste de vehicles récupérée avec succès.",
                "data": vehicles_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucun vehicle trouvé.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération de la liste des vehicles.",
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

@routes_vehicles.route("<int:id>", methods=["GET"])
def get_one_vehicle(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, vehicle_class FROM vehicles WHERE id = %s", (id,))
        vehicle_rows = cursor.fetchall()

        if vehicle_rows:
            response_data = {
                "status": "success",
                "message": "vehicle récupéré avec succès.",
                "data": vehicle_rows
            }
            status_code = 200
        else:
            response_data = {
                "status": "success",
                "message": "Aucun vehicle trouvé.",
                "data": []
            }
            status_code = 200
        
    except Exception as e:
        response_data = {
            "status": "error",
            "message": "Échec de la récupération du vehicle.",
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


@routes_vehicles.route("", methods=["POST"])
def create_one_vehicle():
    return {"create":"a faire"}


@routes_vehicles.route("<int:id>", methods=["DELETE"])
def delete_one_vehicle(id):
    return {"delete":"a faire"}

@routes_vehicles.route("<int:id>", methods=["PUT"])
def update_one_vehicle(id):
    return {"update":"a faire"}