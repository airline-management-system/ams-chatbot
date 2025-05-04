from flask import request,jsonify
from application.api import bp
from application.config import Config
from application.model.client import GeminiClient
from application.model.llm import query_model as get_query_model


@bp.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@bp.route('/generate', methods=['GET'])
def generate():
    model = GeminiClient()
    response = model.generate_response(prompt="give me the top 3 cheapest flights from izmir to istanbul in june")
    return response

@bp.route('/query_model', methods=['GET'])
def query_model():   
    response = get_query_model()
    return response