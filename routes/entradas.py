from flask import Blueprint, jsonify, request
from routes.auth_middleware import token_required



entradas_pb = Blueprint('entradas', __name__)

@entradas_pb.route('/entradas', methods=['POST'])
@token_required
def registrar_entrada():
    from app import supabase
    data = request.get_json()
    
    # 1. Extraer datos del objeto recibido
    cabecera = data.get('cabecera')
    items = data.get('items')

    try:
        # 2. Insertar en la tabla "entradas"
        # Usamos .execute() para obtener el ID de la entrada creada
        nueva_entrada = supabase.table('entradas').insert({
            "id_proveedor": cabecera['id_proveedor'],
            "factura": cabecera['no_factura'],
            "monto_factura": cabecera['total_factura'],
            "fecha_compra": cabecera['fecha_compra'], 
            "id_clinica": cabecera['id_clinica']
        }).execute()

        # Obtenemos el ID generado por Supabase
        id_entrada_generada = nueva_entrada.data[0]['id']

        # 3. Preparar los items para la tabla "detalle_entrada"
        lista_detalles = []
        for item in items:
            lista_detalles.append({
                "id_entrada": id_entrada_generada,
                "id_articulo": item['articulo_id'],
                "cantidad": item['cantidad'],
                "costo_empaque": item['costo_unitario'],
                "lote": item['lote'],
                "fecha_caducidad" : item['fecha_caducidad']
            })

        # 4. Inserción masiva (bulk insert) en "detalle_entrada"
        supabase.table('detalle_entrada').insert(lista_detalles).execute()

        return jsonify({
            "status": "success",
            "message": f"Entrada #{id_entrada_generada} registrada correctamente con {len(items)} artículos."
        }), 201

    except Exception as e:
        print(f"Error en BD: {e}")
        return jsonify({
            "status": "error",
            "message": "No se pudo registrar la entrada",
            "detalles": str(e)
        }), 500