import logging
from datetime import datetime
from .main_menu_handler import MainMenuHandler
from .settings_handler import SettingsHandler
from .user_handler import UserHandler
from api.persistence.mongo.user_messages_persistence import UserMessagesPersistence
from api.persistence.mongo.user_draft_persistence import UserDraftPersistence
from api.persistence.redis.redis_persistence import RedisPersistence
from ..static.whats_iteration_messages import *
from ..static.state import *
from ..static.properties import *

logger = logging.getLogger(__name__)


class WhatsappMessageHandler:

    def __init__(self, db_connection, redis_client):
        self.db = db_connection
        self.redis_client = redis_client
        self.user_messages_persistence = UserMessagesPersistence(self.db)
        self.user_draft_persistence = UserDraftPersistence(self.db)
        self.redis_persistence = RedisPersistence(self.redis_client)

        self.main_menu_handler = MainMenuHandler(self.db, self.redis_client)
        self.settings_handler = SettingsHandler(self.db, self.redis_client)
        self.user_handler = UserHandler(self.db, self.redis_client)

    def handle_whatsapp_message(self, incoming_message, sender) -> 'str | list[str]':
        logger.debug(f'Message received from {sender} - {incoming_message}')

        try:
            user_state = self.redis_persistence.get_state(key=sender)

            self.user_messages_persistence.save_whatsapp_message_history(
                sender=sender,
                message_text=incoming_message,
                timestamp=datetime.now(),
                state=user_state
            )

            if user_state is None:
                # very first time accessing our services
                self.redis_persistence.set_state(
                    key=sender,
                    value=MAIN_STATE
                )
                return WELCOME_MESSAGE

            if user_state == MAIN_STATE:
                return self.main_menu_handler.handle_main_message(incoming_message, sender)
            elif user_state == SETTINGS_STATE:
                return self.settings_handler.handle_settings_message(incoming_message, sender)
            # Updating Name
            elif user_state == NAME_SET_CONFIG_STATE:
                return self.user_handler.request_data_update(user_state, incoming_message, sender, NAME)
            elif user_state == NAME_SET_CONFIRM_STATE:
                return self.user_handler.confirm_new_value(user_state, incoming_message, sender, NAME)
            elif user_state == NAME_SET_PERSIST_STATE:
                return self.user_handler.persist_user_value(incoming_message, sender, NAME)
            # Updating EMAIL
            elif user_state == EMAIL_SET_CONFIG_STATE:
                return self.user_handler.request_data_update(user_state, incoming_message, sender, EMAIL)
            elif user_state == EMAIL_SET_CONFIRM_STATE:
                return self.user_handler.confirm_new_value(user_state, incoming_message, sender, EMAIL)
            elif user_state == EMAIL_SET_PERSIST_STATE:
                return self.user_handler.persist_user_value(incoming_message, sender, EMAIL)

        except Exception as e:
            logger.error(f"ERROR - an error occurred when processing user {sender} with message {incoming_message}: {e}")

        # If none of the actions above happened, restart the state to MAIN
        self.redis_persistence.set_state(
            key=sender,
            value=MAIN_STATE
        )
        self.user_draft_persistence.delete_all_drafts(sender)
        return ["An error happened when processing your request, we are restarting your conversation",
                MAIN_MENU_OPTIONS]
