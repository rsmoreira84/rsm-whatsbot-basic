import unittest
from unittest.mock import MagicMock
from api.handlers.settings_handler import SettingsHandler

from api.static.whats_iteration_messages import *
from api.static.state import *
from api.static.properties import *


class TestSettingsHandler(unittest.TestCase):

    def setUp(self):
        # Mock database and Redis connections
        self.mock_db_connection = MagicMock()
        self.mock_redis_client = MagicMock()

        # Instantiate MainMenuHandler with mocked dependencies
        self.handler = SettingsHandler(self.mock_db_connection, self.mock_redis_client)

        # Mock the persistence objects within the handler
        self.handler.user_persistence = MagicMock()
        self.handler.user_draft_persistence = MagicMock()
        self.handler.redis_persistence = MagicMock()

    def test_handle_settings_message_invalid_input(self):
        """Test that an invalid message returns SETTINGS_OPTIONS."""
        message = "invalid_input"
        sender = "12345"
        result = self.handler.handle_settings_message(message, sender)
        assert result == SETTINGS_OPTIONS

    def test_handle_settings_message_return_to_main(self):
        """Test that option 0 sets the state to MAIN_STATE and returns the main menu."""
        message = "0"
        sender = "12345"
        result = self.handler.handle_settings_message(message, sender)

        self.handler.redis_persistence.set_state.assert_called_once_with(
            key=sender, value=MAIN_STATE
        )
        assert result == MAIN_MENU_OPTIONS

    def test_handle_settings_message_update_name_set(self):
        """Test that option 1 sets the state to NAME_SET_CONFIG_STATE and returns the update message with the user's name."""
        message = "1"
        sender = "12345"
        mock_user = {NAME: "Test User"}

        self.handler.user_persistence.find_user.return_value = mock_user

        result = self.handler.handle_settings_message(message, sender)

        self.handler.redis_persistence.set_state.assert_called_once_with(
            key=sender, value=NAME_SET_CONFIG_STATE
        )
        self.handler.user_persistence.find_user.assert_called_once_with(sender)
        assert result == PROPERTY_UPDATE_OPTIONS.format(NAME, "Test User")

    def test_handle_settings_message_update_name_not_set(self):
        """Test that option 1 returns 'Not set' if the name is not in the user data."""
        message = "1"
        sender = "12345"
        mock_user = {}  # No name in the user data

        self.handler.user_persistence.find_user.return_value = mock_user

        result = self.handler.handle_settings_message(message, sender)

        self.handler.redis_persistence.set_state.assert_called_once_with(
            key=sender, value=NAME_SET_CONFIG_STATE
        )
        self.handler.user_persistence.find_user.assert_called_once_with(sender)
        assert result == PROPERTY_UPDATE_OPTIONS.format(NAME, "Not set")

    def test_handle_settings_message_update_email_set(self):
        """Test that option 2 sets the state to EMAIL_SET_CONFIG_STATE and returns the update message with the user's email."""
        message = "2"
        sender = "12345"
        mock_user = {EMAIL: "test@example.com"}

        self.handler.user_persistence.find_user.return_value = mock_user

        result = self.handler.handle_settings_message(message, sender)

        self.handler.redis_persistence.set_state.assert_called_once_with(
            key=sender, value=EMAIL_SET_CONFIG_STATE
        )
        self.handler.user_persistence.find_user.assert_called_once_with(sender)
        assert result == PROPERTY_UPDATE_OPTIONS.format(EMAIL, "test@example.com")

    def test_handle_settings_message_update_email_not_set(self):
        """Test that option 2 returns 'Not set' if the email is not in the user data."""
        message = "2"
        sender = "12345"
        mock_user = {}  # No email in the user data

        self.handler.user_persistence.find_user.return_value = mock_user

        result = self.handler.handle_settings_message(message, sender)

        self.handler.redis_persistence.set_state.assert_called_once_with(
            key=sender, value=EMAIL_SET_CONFIG_STATE
        )
        self.handler.user_persistence.find_user.assert_called_once_with(sender)
        assert result == PROPERTY_UPDATE_OPTIONS.format(EMAIL, "Not set")

    def test_handle_settings_message_delete_user_data(self):
        """Test that option 3 deletes user data and returns the confirmation message."""
        message = "3"
        sender = "12345"
        result = self.handler.handle_settings_message(message, sender)

        self.handler.redis_persistence.set_state.assert_called_once_with(
            key=sender, value=MAIN_STATE
        )
        self.handler.user_draft_persistence.delete_all_drafts.assert_called_once_with(
            sender
        )
        self.handler.user_persistence.delete_user.assert_called_once_with(sender)
        assert result == USER_DATA_DELETED_MESSAGE

    def test_handle_settings_message_unknown_option(self):
        """Test that an unknown integer message returns SETTINGS_OPTIONS."""
        message = "99"
        sender = "12345"
        result = self.handler.handle_settings_message(message, sender)
        assert result == SETTINGS_OPTIONS
        # Verify that no persistence methods were called
        self.handler.redis_persistence.set_state.assert_not_called()
        self.handler.user_persistence.find_user.assert_not_called()
        self.handler.user_draft_persistence.delete_all_drafts.assert_not_called()
        self.handler.user_persistence.delete_user.assert_not_called()


if __name__ == '__main__':
    unittest.main()
