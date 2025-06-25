import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host = os.environ.get("DB_HOST"), 
        user = os.environ.get("DB_USER"), 
        password = os.environ.get("DB_PASSWORD"), 
        database = os.environ.get("DB_NAME"),
        autocommit = False,  # manejamos transacciones manualmente
        use_pure=True
    )