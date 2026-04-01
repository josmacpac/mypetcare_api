from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from app import supabase
        
        # 1. Buscar la cabecera de Authorization
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Token de autenticación faltante"
            }), 401
            
        try:
            # 2. El header viene como "Bearer <token>", separamos la palabra Bearer
            token = auth_header.split(" ")[1]
            
            # 3. Le preguntamos a Supabase si el token es válido
            user_response = supabase.auth.get_user(token)
            
            # 4. Si es válido, guardamos los datos del usuario en el contexto por si los necesitas
            request.user = user_response.user
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Token inválido o expirado",
                "detalles": str(e)
            }), 401
            
        return f(*args, **kwargs)
        
    return decorated