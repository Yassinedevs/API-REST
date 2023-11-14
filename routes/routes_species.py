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

