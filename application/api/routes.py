from flask import jsonify
from application.api import bp
from application.config import Config

@bp.route('/ping', methods=['GET'])
def ping():
    return 'pong'