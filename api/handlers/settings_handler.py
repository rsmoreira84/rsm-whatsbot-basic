import logging
from ..static.whats_iteration_messages import *
from api.persistence.mongo.user_persistence import UserPersistence
from api.persistence.redis.redis_persistence import RedisPersistence
from api.persistence.mongo.user_draft_persistence import UserDraftPersistence
from ..static.state import *
from ..static.properties import *

logger = logging.getLogger(__name__)


class SettingsHandler:

    def __init__(self, connection_db, redis_client):
        self.user_persistence = UserPersistence(connection_db)
        self.user_draft_persistence = UserDraftPersistence(connection_db)
        self.redis_persistence = RedisPersistence(redis_client)

    def handle_settings_message(self, message, sender):
        logger.debug(f"Sender {sender} - message {message}")

        try:
            user_option = int(message)
        except Exception as e:
            return SETTINGS_OPTIONS

        state = None
        prop = None

        match user_option:
            # return to main
            case 0:
                self.redis_persistence.set_state(
                    key=sender,
                    value=MAIN_STATE
                )
                return MAIN_MENU_OPTIONS
            # Update name
            case 1:
                state = NAME_SET_CONFIG_STATE
                prop = NAME
            # Update Email
            case 2:
                state = EMAIL_SET_CONFIG_STATE
                prop = EMAIL
            # Delete all user info data
            case 3:
                self.redis_persistence.set_state(
                    key=sender,
                    value=MAIN_STATE
                )
                self.user_draft_persistence.delete_all_drafts(sender)
                self.user_persistence.delete_user(sender)

                return USER_DATA_DELETED_MESSAGE

        if state is not None and prop is not None:
            self.redis_persistence.set_state(
                key=sender,
                value=state
            )
            user = self.user_persistence.find_user(sender)
            if user is not None and \
                    prop in user and \
                    user[prop] is not None:
                value = user[prop]
            else:
                value = "Not set"
            return PROPERTY_UPDATE_OPTIONS.format(prop, value)

        return SETTINGS_OPTIONS
