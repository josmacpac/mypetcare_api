from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from app import supabase
        
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Token de autenticación faltante"
            }), 401
            
        try:
            
            token = auth_header.split(" ")[1]
            user_response = supabase.auth.get_user(token)
            request.user = user_response.user
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Token inválido o expirado",
                "detalles": str(e)
            }), 401
            
        return f(*args, **kwargs)
        
    return decorated


def token_required_with_clinic(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from app import supabase
        
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Token de autenticación faltante"
            }), 401
            
        try:
            token = auth_header.split(" ")[1]
            user_response = supabase.auth.get_user(token)
            
            # Guardamos el usuario como en el original
            request.user = user_response.user
            
            # Extraemos y guardamos la clínica específicamente
            # Usamos el metadata que ya confirmamos que tienes
            id_clinica = user_response.user.user_metadata.get('id_clinica')
            
            if id_clinica is None:
                return jsonify({
                    "status": "error",
                    "message": "El usuario no tiene una clínica vinculada"
                }), 403
                
            request.id_clinica = id_clinica
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Token inválido o expirado",
                "detalles": str(e)
            }), 401
            
        return f(*args, **kwargs)
        
    return decorated