from flask import Blueprint, jsonify
from ..utils.response_utils import SUCCESS

ping_bp = Blueprint('ping', __name__)

@ping_bp.route('/ping', methods=['GET'])
def ping():
    return SUCCESS("PONG!")
