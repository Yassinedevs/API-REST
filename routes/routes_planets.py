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
