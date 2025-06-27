import unittest
from unittest.mock import MagicMock
from api.handlers.user_handler import UserHandler

from api.static.whats_iteration_messages import *
from api.static.state import *
from api.static.properties import *


class TestUserHandler(unittest.TestCase):

    def setUp(self):
        # Mock database and Redis connections
        self.mock_db_connection = MagicMock()
        self.mock_redis_client = MagicMock()

        # Instantiate MainMenuHandler with mocked dependencies
        # This will create real persistence objects inside it
        self.handler = UserHandler(self.mock_db_connection, self.mock_redis_client)

        # Create the mock persistence objects
        self.mock_user_persistence = MagicMock()
        self.mock_user_draft_persistence = MagicMock()
        self.mock_redis_persistence = MagicMock()

        # Replace the real persistence objects in the handler with our mocks
        self.handler.user_persistence = self.mock_user_persistence
        self.handler.user_draft_persistence = self.mock_user_draft_persistence
        self.handler.redis_persistence = self.mock_redis_persistence

    def test_request_data_update_invalid_message_name_not_set(self):
        """
        Test request_data_update with an invalid message when user name is not set.
        """
        sender = "user123"
        initial_state = "SOME_STATE"
        prop_description = NAME
        invalid_message = "abc"

        # Mock find_user to return a user without the property set
        self.mock_user_persistence.find_user.return_value = {"id": sender, "email": "test@example.com"}

        expected_response = PROPERTY_UPDATE_OPTIONS.format(prop_description, "Not set")

        response = self.handler.request_data_update(initial_state, invalid_message, sender, prop_description)

        self.assertEqual(response, expected_response)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=NAME_SET_CONFIG_STATE
        )
        self.mock_user_persistence.find_user.assert_called_once_with(sender)

    def test_request_data_update_invalid_message_email_set(self):
        """
        Test request_data_update with an invalid message when user email is set.
        """
        sender = "user456"
        initial_state = "SOME_STATE"
        prop_description = EMAIL
        invalid_message = "99"  # Out of range for options 0 or 1

        # Mock find_user to return a user with the property set
        self.mock_user_persistence.find_user.return_value = {"id": sender, "email": "existing@example.com"}

        expected_response = PROPERTY_UPDATE_OPTIONS.format(prop_description, "existing@example.com")

        response = self.handler.request_data_update(initial_state, invalid_message, sender, prop_description)

        self.assertEqual(response, expected_response)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=EMAIL_SET_CONFIG_STATE
        )
        self.mock_user_persistence.find_user.assert_called_once_with(sender)

    def test_request_data_update_option_0_cancel(self):
        """
        Test request_data_update when user selects option 0 (cancel).
        """
        sender = "user789"
        initial_state = "SOME_STATE"
        prop_description = NAME
        message = "0"

        expected_response = SETTINGS_OPTIONS

        response = self.handler.request_data_update(initial_state, message, sender, prop_description)

        self.assertEqual(response, expected_response)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=SETTINGS_STATE
        )
        self.mock_user_persistence.find_user.assert_not_called()  # Should not be called for valid options

    def test_request_data_update_option_1_request_new_name(self):
        """
        Test request_data_update when user selects option 1 (request new name).
        """
        sender = "user101"
        initial_state = "SOME_STATE"
        prop_description = NAME
        message = "1"

        expected_response = PROPERTY_UPDATE_REQUEST_VALUE.format(prop_description, prop_description)

        response = self.handler.request_data_update(initial_state, message, sender, prop_description)

        self.assertEqual(response, expected_response)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=NAME_SET_CONFIRM_STATE
        )
        self.mock_user_persistence.find_user.assert_not_called()

    def test_request_data_update_option_1_request_new_email(self):
        """
        Test request_data_update when user selects option 1 (request new email).
        """
        sender = "user112"
        initial_state = "SOME_STATE"
        prop_description = EMAIL
        message = "1"

        expected_response = PROPERTY_UPDATE_REQUEST_VALUE.format(prop_description, prop_description)

        response = self.handler.request_data_update(initial_state, message, sender, prop_description)

        self.assertEqual(response, expected_response)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=EMAIL_SET_CONFIRM_STATE
        )
        self.mock_user_persistence.find_user.assert_not_called()

    def test_confirm_new_value_name(self):
        """
        Test confirm_new_value for name property.
        """
        sender = "user202"
        initial_state = "SOME_STATE"
        new_value = "John Doe"
        prop_description = NAME

        expected_response = PROPERTY_UPDATE_CONFIRM_MESSAGE.format(prop_description, new_value)

        response = self.handler.confirm_new_value(initial_state, new_value, sender, prop_description)

        self.assertEqual(response, expected_response)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=NAME_SET_PERSIST_STATE
        )
        self.mock_user_draft_persistence.save_draft_data.assert_called_once_with(
            prop_description, sender, new_value
        )

    def test_confirm_new_value_email(self):
        """
        Test confirm_new_value for email property.
        """
        sender = "user303"
        initial_state = "SOME_STATE"
        new_value = "john.doe@example.com"
        prop_description = EMAIL

        expected_response = PROPERTY_UPDATE_CONFIRM_MESSAGE.format(prop_description, new_value)

        response = self.handler.confirm_new_value(initial_state, new_value, sender, prop_description)

        self.assertEqual(response, expected_response)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=EMAIL_SET_PERSIST_STATE
        )
        self.mock_user_draft_persistence.save_draft_data.assert_called_once_with(
            prop_description, sender, new_value
        )

    def test_persist_user_value_invalid_option_with_draft(self):
        """
        Test persist_user_value with an invalid option when a draft exists.
        """
        sender = "user404"
        prop_name = NAME
        message = "invalid"
        draft_value = "DraftName"

        self.mock_user_draft_persistence.find_draft_data.return_value = {"value": draft_value}

        expected_response = PROPERTY_UPDATE_CONFIRM_MESSAGE.format(prop_name, draft_value)

        response = self.handler.persist_user_value(message, sender, prop_name)

        self.assertEqual(response, expected_response)
        self.mock_user_draft_persistence.find_draft_data.assert_called_once_with(prop_name, sender)
        self.mock_redis_persistence.set_state.assert_not_called()
        self.mock_user_persistence.update_user_property.assert_not_called()
        self.mock_user_draft_persistence.delete_draft.assert_not_called()

    def test_persist_user_value_invalid_option_no_draft(self):
        """
        Test persist_user_value with an invalid option when no draft exists.
        """
        sender = "user505"
        prop_name = EMAIL
        message = "3"  # Out of range for 0, 1, 2

        self.mock_user_draft_persistence.find_draft_data.return_value = None

        expected_response = PROPERTY_UPDATE_CONFIRM_MESSAGE.format(prop_name, "-not informed-")

        response = self.handler.persist_user_value(message, sender, prop_name)

        self.assertEqual(response, expected_response)
        self.mock_user_draft_persistence.find_draft_data.assert_called_once_with(prop_name, sender)
        self.mock_redis_persistence.set_state.assert_not_called()
        self.mock_user_persistence.update_user_property.assert_not_called()
        self.mock_user_draft_persistence.delete_draft.assert_not_called()

    def test_persist_user_value_option_0_cancel(self):
        """
        Test persist_user_value when user selects option 0 (cancel).
        """
        sender = "user606"
        prop_name = NAME
        message = "0"

        self.mock_user_draft_persistence.find_draft_data.return_value = {"value": "SomeDraft"}

        expected_response = SETTINGS_OPTIONS

        response = self.handler.persist_user_value(message, sender, prop_name)

        self.assertEqual(response, expected_response)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=SETTINGS_STATE
        )
        self.mock_user_draft_persistence.delete_draft.assert_called_once_with(sender, prop_name)
        self.mock_user_persistence.update_user_property.assert_not_called()

    def test_persist_user_value_option_1_save_success(self):
        """
        Test persist_user_value when user selects option 1 (save) and draft exists.
        """
        sender = "user707"
        prop_name = NAME
        message = "1"
        draft_value = "NewUserName"

        self.mock_user_draft_persistence.find_draft_data.return_value = {"value": draft_value}

        expected_update_msg = "*Updating name*\nUser name successfully updated."
        expected_response = [expected_update_msg, SETTINGS_OPTIONS]

        response = self.handler.persist_user_value(message, sender, prop_name)

        self.assertEqual(response, expected_response)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=SETTINGS_STATE
        )
        self.mock_user_persistence.update_user_property.assert_called_once_with(sender, draft_value, prop_name)
        # Verify both calls to delete_draft as per original code's logic
        self.assertEqual(self.mock_user_draft_persistence.delete_draft.call_count, 2)
        # The original code calls delete_draft(sender, NAME) even if prop_name is EMAIL
        # This reflects that behavior.
        self.mock_user_draft_persistence.delete_draft.assert_any_call(sender, NAME)
        self.mock_user_draft_persistence.delete_draft.assert_any_call(sender, prop_name)
        # Ensure the final call is with prop_name, as it's the second one for prop_name
        # if prop_name is not NAME.
        self.mock_user_draft_persistence.delete_draft.assert_called_with(sender, prop_name)

    def test_persist_user_value_option_1_save_no_draft_value(self):
        """
        Test persist_user_value when user selects option 1 (save) but no draft value is found.
        """
        sender = "user808"
        prop_name = EMAIL
        message = "1"

        # Mock find_draft_data to return a dict without 'value' or None
        self.mock_user_draft_persistence.find_draft_data.return_value = {"some_other_key": "data"}

        expected_error_msg = "*Updating email*\nError updating email."
        expected_response = [expected_error_msg, SETTINGS_OPTIONS]

        response = self.handler.persist_user_value(message, sender, prop_name)

        self.assertEqual(response, expected_response)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=SETTINGS_STATE
        )
        self.mock_user_persistence.update_user_property.assert_not_called()
        self.assertEqual(self.mock_user_draft_persistence.delete_draft.call_count, 1)
        self.mock_user_draft_persistence.delete_draft.assert_any_call(sender, prop_name)

    def test_persist_user_value_option_2_inform_again(self):
        """
        Test persist_user_value when user selects option 2 (inform again).
        """
        sender = "user909"
        prop_name = NAME
        message = "2"

        self.mock_user_draft_persistence.find_draft_data.return_value = {"value": "OldDraft"}

        expected_response = PROPERTY_UPDATE_REQUEST_VALUE.format(prop_name, prop_name)

        response = self.handler.persist_user_value(message, sender, prop_name)

        if prop_name == NAME:
            expected_state = NAME_SET_CONFIRM_STATE
        elif prop_name == EMAIL:
            expected_state = EMAIL_SET_CONFIRM_STATE

        self.assertEqual(response, expected_response)
        # Note: Original code calls delete_draft(sender, NAME) regardless of prop_name
        self.mock_user_draft_persistence.delete_draft.assert_called_once_with(sender, prop_name)
        self.mock_redis_persistence.set_state.assert_called_once_with(
            key=sender, value=expected_state
        )
        self.mock_user_persistence.update_user_property.assert_not_called()


if __name__ == '__main__':
    unittest.main()
