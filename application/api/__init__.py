from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Make sure the routes execute
import application.api.routes