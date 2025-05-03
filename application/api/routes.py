from flask import request,jsonify
from application.api import bp
from application.config import Config
from application.model.client import GeminiClient


@bp.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@bp.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    # Check if 'prompt' exists in the request body
    if not data or 'prompt' not in data:
        return jsonify({'error': 'Prompt is required in the request body'}), 400
    
    model = GeminiClient()
    response = model.generate_response(prompt=data.prompt)
    return response