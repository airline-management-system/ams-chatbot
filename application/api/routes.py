from flask import request,jsonify
from application.api import bp
from application.model.client import GeminiClient
from application.mcp.client import MCPClient
from application.model.prompt_manager import PromptManager


@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Service is running'
    }), 200


@bp.route('/query_model', methods=['POST'])
async def query_model():
    data = request.get_json()['prompt']
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    history = request.get_json()['history']
    mcp_client = MCPClient()
    response = await mcp_client.process_query(data,history)

    return response


@bp.route('/crm', methods=['POST'])
def crm():
    data = str(request.get_json()['prompt'])
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    client = GeminiClient()
    prompt_manager = PromptManager()
    response = client.generate_response(prompt=prompt_manager.crm_prompt(data))

    return response