from flask import request,jsonify
from application.api import bp
from application.config import Config
from application.model.client import GeminiClient
from application.model.llm import query_model as get_query_model, similarity_search
from application.middlewares.auth import token_required


@bp.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@bp.route('/generate', methods=['POST'])
#@token_required
def generate():
    data = request.get_json()['prompt']
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    response = similarity_search(prompt=data)
    return response

@bp.route('/query_model', methods=['POST'])
#@token_required
def query_model():
    data = request.get_json()['prompt']
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
        
    response = get_query_model(prompt=data)
    return response