from flask import Blueprint, jsonify, request
from routes.auth_middleware import token_required



articulos_pb = Blueprint('articulos', __name__)

@articulos_pb.route('/articulos', methods=['GET'])
@token_required
def get_articulos():
    from app import supabase
    try:
        # Usamos alias (nombre_que_quiero:columna_original) para evitar conflictos
        # Estructura: tabla_relacionada(alias:columna_de_la_otra_tabla)
        query = """
            *,
            cat_info:categoria_articulos(nombre_categoria),
            pres_info:presentacion(presentacion)
        """
        
        response = supabase.table('articulos').select(query).execute()
        
        return jsonify({
            "status": "success",
            "message": "¡Lista de artículos sincronizada!",
            "data": response.data
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Error al realizar el Join en la base de datos",
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


