from flask import Blueprint, jsonify, request
from routes.auth_middleware import token_required_with_clinic



existencias_pb = Blueprint('existencias', __name__)



@existencias_pb.route('/existencias', methods=['GET'])
@token_required_with_clinic
def obtener_existencia():
    from app import supabase
    try:
        # Llamamos a la vista que creaste en el SQL Editor
        # Supabase trata las vistas exactamente igual que las tablas para consultas SELECT
        response = supabase.table('vista_resumen_inventario') \
            .select("*") \
            .eq('id_clinica', request.id_clinica) \
            .execute()
        
        return jsonify(response.data), 200
    except Exception as e:
        print(f"Error al obtener inventario: {e}")
        return jsonify({"error": "No se pudo cargar el inventario"}), 500

@existencias_pb.route('/existencias/lotes/<int:articulo_id>', methods=['GET'])
@token_required_with_clinic
def obtener_lotes_por_articulo(articulo_id):
    from app import supabase
    try:
        # Consultamos la vista filtrando por el id_articulo
        response = supabase.table('vista_detalle_lotes') \
            .select("*") \
            .eq('id_articulo', articulo_id) \
            .eq('id_clinica', request.id_clinica) \
            .execute()
        
        return jsonify(response.data), 200
    except Exception as e:
        print(f"Error en lotes: {e}")
        return jsonify({"error": "No se pudieron obtener los lotes"}), 500
    
@existencias_pb.route('/reporte-caducidad', methods=['GET'])
@token_required_with_clinic
def obtener_reporte_caducidad():
    from app import supabase
    try:
        # Consultamos la vista de caducidades
        response = supabase.table('vista_reporte_caducidad') \
            .select("*") \
            .eq('id_clinica', request.id_clinica) \
            .execute()
        return jsonify(response.data), 200
    except Exception as e:
        print(f"Error en reporte caducidad: {e}")
        return jsonify({"error": "No se pudo generar el reporte"}), 500
    
    ##Se actualizan vistas en supabase para filtrar por id_clinica
    