import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route("/test")
def test():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, title, producer FROM films")
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


if __name__ == "__main__":
    app.run()