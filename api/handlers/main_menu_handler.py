import logging
from ..static.whats_iteration_messages import *
from api.persistence.mongo.user_persistence import UserPersistence
from api.persistence.redis.redis_persistence import RedisPersistence
from ..static.state import SETTINGS_STATE
from ..utils.user_info import build_user_info_message

logger = logging.getLogger(__name__)


class MainMenuHandler:

    def __init__(self, db_connection, redis_client):
        self.user_persistence = UserPersistence(db_connection)
        self.redis_persistence = RedisPersistence(redis_client)

    def handle_main_message(self, message, sender):
        try:
            user_option = int(message)
        except Exception as e:
            # message wasn't parsed, so it's a text. Returning main options
            return MAIN_MENU_OPTIONS

        logger.debug(f'user {sender} option {user_option}')

        match user_option:
            # Contact Us
            case 1:
                return CONTACT_US_MESSAGE
            # User Info
            case 2:
                user = self.user_persistence.find_user(sender)
                if user is None:
                    return NO_USER_INFO_MESSAGE
                else:
                    return build_user_info_message(user)
            # Settings
            case 3:
                self.redis_persistence.set_state(
                    key=sender,
                    value=SETTINGS_STATE
                )
                return SETTINGS_OPTIONS

        return MAIN_MENU_OPTIONS
