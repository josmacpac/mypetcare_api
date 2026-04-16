from flask import Blueprint, jsonify, request
from routes.auth_middleware import token_required



entradas_pb = Blueprint('entradas', __name__)

@entradas_pb.route('/entradas', methods=['POST'])
@token_required
def post_entrada():
    from app import supabase
    print("agregando entrada al inventaio...")