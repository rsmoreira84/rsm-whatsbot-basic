from flask import Blueprint, request, current_app
from twilio.twiml.messaging_response import MessagingResponse
from ..handlers.whatsbot_handler import WhatsappMessageHandler
from ..utils.custom_exception import GeneralAppError
import logging

logger = logging.getLogger(__name__)

whatsbot_bp = Blueprint('whatsbot', __name__)


@whatsbot_bp.route("/", methods=["get", "post"])
def reply():
    message_text = request.form.get("Body")
    phone_number = request.form.get("From")

    response = MessagingResponse()

    try:
        whatsapp_handler = WhatsappMessageHandler(current_app.db, current_app.redis_client)
        response.message(whatsapp_handler.handle_whatsapp_message(message_text, phone_number))
        return str(response)
    except GeneralAppError as e:
        logger.error(f"ERROR occurred when processing Whatsapp message: {e}")
        response.message("An error has occurred")
    except Exception as e:
        logger.error(f"ERROR occurred when processing Whatsapp message: {e}")
        response.message("An error has occurred")
    finally:
        return str(response)
