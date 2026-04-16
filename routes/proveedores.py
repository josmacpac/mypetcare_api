from flask import Blueprint, jsonify, request
from routes.auth_middleware import token_required



proveedores_pb = Blueprint('proveedores', __name__)

@proveedores_pb.route('/proveedores', methods=['GET'])
@token_required
def get_provedores():
    from app import supabase
    try:
        
        
        response = supabase.table('proveedores').select('*').execute()
        
        return jsonify({
            "status": "success",
            "message": "¡Lista de Proveedores sincronizada!",
            "data": response.data
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Error al obtener datos de la base de datos",
            "detalles": str(e)
        }), 500

@proveedores_pb.route('/laboratorio', methods=['GET'])
@token_required
def get_laboratorio():
    from app import supabase
    try:
        
        
        response = supabase.table('laboratorio').select('*').execute()
        
        return jsonify({
            "status": "success",
            "message": "¡Lista de laboratorios sincronizada!",
            "data": response.data
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Error al obtener datos de la base de datos",
            "detalles": str(e)
        }), 500