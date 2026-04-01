import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from supabase import create_client, Client


# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Inicializar el cliente de Supabase
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Faltan las credenciales de Supabase en las variables de entorno.")

supabase: Client = create_client(supabase_url, supabase_key)


# --------------------------------------------------
# REGISTRO DE RUTAS (BLUEPRINTS)
# --------------------------------------------------
from routes.test import test_pb
from routes.articulos import articulos_pb


app.register_blueprint(test_pb, url_prefix='/api')
app.register_blueprint(articulos_pb, url_prefix='/api')

if __name__ == '__main__':
    # Flask correrá en el puerto 5000 por defecto
    app.run(debug=True, port=5000)