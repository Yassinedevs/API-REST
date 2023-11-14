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
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print("ddddddddddd")
        print(e)
    finally:
        cursor.close() 
        conn.close()  
