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