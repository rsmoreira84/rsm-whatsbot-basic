from flask import Blueprint

routes = Blueprint('routes', __name__)

from api.endpoints.ping import ping_bp
from api.endpoints.whatsbot import whatsbot_bp
from api.endpoints.whatsbot_http_sim import whatsbot_sim_bp

routes.register_blueprint(ping_bp)
routes.register_blueprint(whatsbot_bp)
routes.register_blueprint(whatsbot_sim_bp)