#AJUSTA DATOS A DATABASE LOCAL

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="", 
        database="ludoteca",
        autocommit=False,  # manejamos transacciones manualmente
        use_pure=True
    )