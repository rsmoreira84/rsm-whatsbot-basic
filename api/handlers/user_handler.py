import logging
from ..static.whats_iteration_messages import *
from api.persistence.mongo.user_persistence import UserPersistence
from api.persistence.mongo.user_draft_persistence import UserDraftPersistence
from api.persistence.redis.redis_persistence import RedisPersistence
from ..static.state import *
from ..static.properties import *

logger = logging.getLogger(__name__)


class UserHandler:
    def __init__(self, connection_db, redis_client):
        self.user_persistence = UserPersistence(connection_db)
        self.user_draft_persistence = UserDraftPersistence(connection_db)
        self.redis_persistence = RedisPersistence(redis_client)

    def request_data_update(self, state, message, sender, prop_description):
        logger.debug(f"User {sender} - Message {message} - state {state}")
        try:
            user_option = int(message)
            invalid_value = user_option < 0 or user_option > 1
        except Exception as e:
            invalid_value = True

        if invalid_value:
            if prop_description == NAME:
                state = NAME_SET_CONFIG_STATE
            elif prop_description == EMAIL:
                state = EMAIL_SET_CONFIG_STATE

            self.redis_persistence.set_state(
                key=sender,
                value=state
            )
            user = self.user_persistence.find_user(sender)
            if user is not None and \
                    prop_description in user and\
                    user[prop_description] is not None:
                value = user[prop_description]
            else:
                value = "Not set"
            return PROPERTY_UPDATE_OPTIONS.format(prop_description, value)

        match user_option:
            case 0:
                self.redis_persistence.set_state(
                    key=sender,
                    value=SETTINGS_STATE
                )
                return SETTINGS_OPTIONS
            case 1:
                if prop_description == NAME:
                    state = NAME_SET_CONFIRM_STATE
                elif prop_description == EMAIL:
                    state = EMAIL_SET_CONFIRM_STATE

                self.redis_persistence.set_state(
                    key=sender,
                    value=state
                )
                return PROPERTY_UPDATE_REQUEST_VALUE.format(prop_description, prop_description)

    def confirm_new_value(self, state, message, sender, prop_description):
        logger.debug(f"User {sender} - Message {message} - state {state}")

        if prop_description == NAME:
            state = NAME_SET_PERSIST_STATE
        elif prop_description == EMAIL:
            state = EMAIL_SET_PERSIST_STATE

        self.redis_persistence.set_state(
            key=sender,
            value=state
        )

        self.user_draft_persistence.save_draft_data(prop_description, sender, message)

        return PROPERTY_UPDATE_CONFIRM_MESSAGE.format(prop_description, message)

    def persist_user_value(self, message, sender, prop_description):
        logger.debug(f"User {sender} - Message {message} - prop {prop_description}")

        draft = self.user_draft_persistence.find_draft_data(prop_description, sender)

        try:
            user_option = int(message)
            invalid_option = user_option < 0 or user_option > 2
        except Exception as e:
            invalid_option = True

        if invalid_option:
            # Wrong option informed
            if draft is not None and draft["value"] is not None:
                response_msg = PROPERTY_UPDATE_CONFIRM_MESSAGE.format(prop_description, draft["value"])
            else:
                response_msg = PROPERTY_UPDATE_CONFIRM_MESSAGE.format(prop_description, "-not informed-")
            return response_msg

        match user_option:
            case 0:
                # Cancel updating Prop, get back to Settings Menu
                self.redis_persistence.set_state(
                    key=sender,
                    value=SETTINGS_STATE
                )

                self.user_draft_persistence.delete_draft(sender, prop_description)

                return SETTINGS_OPTIONS
            case 1:
                # Save Prop, then back to settings
                self.redis_persistence.set_state(
                    key=sender,
                    value=SETTINGS_STATE
                )

                if draft is not None and \
                        "value" in draft and \
                        draft["value"] is not None:
                    self.user_persistence.update_user_property(sender, draft["value"], prop_description)
                    self.user_draft_persistence.delete_draft(sender, prop_description)
                    response = "*Updating {}*\n" \
                               "User {} successfully updated.".format(prop_description, prop_description)
                else:
                    response = "*Updating {}*\n" \
                               "Error updating {}.".format(prop_description, prop_description)

                self.user_draft_persistence.delete_draft(sender, prop_description)

                return [response, SETTINGS_OPTIONS]

            case 2:
                # User wants to inform the name again
                self.user_draft_persistence.delete_draft(sender, prop_description)

                if prop_description == NAME:
                    state = NAME_SET_CONFIRM_STATE
                elif prop_description == EMAIL:
                    state = EMAIL_SET_CONFIRM_STATE

                self.redis_persistence.set_state(
                    key=sender,
                    value=state
                )

                return PROPERTY_UPDATE_REQUEST_VALUE.format(prop_description, prop_description)
