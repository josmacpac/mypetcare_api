from flask import Blueprint, jsonify

test_pb = Blueprint('test', __name__)

@test_pb.route('/test-conexion', methods=['GET'])
def probar_supabase():
    from app import supabase

    try:
        # Intentamos consultar 1 solo registro de usuarios
        # (Si la tabla está vacía, no importa, regresará un arreglo [])
        response = supabase.table('usuarios').select("*").limit(1).execute()
        
        return jsonify({
            "status": "success",
            "message": "¡Blueprint y conexión a Supabase funcionando al 100%!",
            "data": response.data
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Error en la conexión o en el Blueprint",
            "detalles": str(e)
        }), 500