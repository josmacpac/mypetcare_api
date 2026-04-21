from flask import Blueprint, jsonify, request
from routes.auth_middleware import token_required



existencias_pb = Blueprint('existencias', __name__)



@existencias_pb.route('/existencias', methods=['GET'])
@token_required
def obtener_existencia():
    from app import supabase
    try:
        # Llamamos a la vista que creaste en el SQL Editor
        # Supabase trata las vistas exactamente igual que las tablas para consultas SELECT
        response = supabase.table('vista_resumen_inventario').select("*").execute()
        
        return jsonify(response.data), 200
    except Exception as e:
        print(f"Error al obtener inventario: {e}")
        return jsonify({"error": "No se pudo cargar el inventario"}), 500