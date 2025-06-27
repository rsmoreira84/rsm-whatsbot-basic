from flask import Blueprint, request, current_app
from ..handlers.whatsbot_handler import WhatsappMessageHandler
from ..utils.response_utils import BAD_REQUEST, SUCCESS, INTERNAL_ERROR
from ..utils.custom_exception import GeneralAppError
import logging

logger = logging.getLogger(__name__)

whatsbot_sim_bp = Blueprint('whatsbot_sim', __name__)


@whatsbot_sim_bp.route("/http-sim", methods=["get", "post"])
def reply():
    if not request.is_json:
        return BAD_REQUEST("Request must be a JSON")

    data = request.json

    From = data.get("from")
    Body = data.get("body")

    if From is None or Body is None:
        return BAD_REQUEST("Missing property 'from' or 'body' in the request body")

    try:
        whatsapp_handler = WhatsappMessageHandler(current_app.db, current_app.redis_client)
        handler_response = whatsapp_handler.handle_whatsapp_message(Body, From)
        if isinstance(handler_response, list):
            response = " :: ".join(handler_response)
        else:
            response = handler_response

        return SUCCESS(response)
    except GeneralAppError as e:
        logger.error(f"ERROR at whatsbot_sim route: {e}")
        return BAD_REQUEST("Your request resulted in a error")
    except Exception as e:
        logger.error(f"ERROR at whatsbot_sim route: {e}")
        return INTERNAL_ERROR()
