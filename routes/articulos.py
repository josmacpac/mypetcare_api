from flask import Blueprint, jsonify, request
from routes.auth_middleware import token_required



articulos_pb = Blueprint('articulos', __name__)

@articulos_pb.route('/articulos', methods=['GET'])
@token_required
def get_articulos():
    from app import supabase
    try:
        # Intentamos consultar registro de articulos
        # (Si la tabla está vacía, no importa, regresará un arreglo [])
        response = supabase.table('articulos').select("*").execute()
        
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

@articulos_pb.route('/articulos', methods=['POST'])
@token_required
def post_articulo():
    from app import supabase
    try:
        data = request.get_json()

        campos_requeridos = [
            'sku', 'nombre_articulo', 'presentacion', 
            'categoria_articulo', 'contenido_empaque', 
            'stock_minimo', 'precio_venta'
        ]

        campos_faltantes = [campo for campo in campos_requeridos if campo not in data]

        if campos_faltantes:
            return jsonify({
                "status": "error",
                "message": f"Faltan campos obligatorios: {', '.join(campos_faltantes)}"
            }), 400

        response = supabase.table('articulos').insert({
                "sku": data['sku'], 
                "nombre_articulo": data['nombre_articulo'],
                "categoria_articulo": data["categoria_articulo"],
                "contenido_empaque": data["contenido_empaque"],
                "stock_minimo": data["stock_minimo"],
                "precio_venta": data["precio_venta"],
                "presentacion": data["presentacion"]

        }).execute()      
        return jsonify({
            "status": "success",
            "message": "¡Articulos ingresado",
            "data": response.data
        }), 201
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "detalles": str(e)
        }), 500


