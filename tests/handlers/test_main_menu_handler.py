import unittest
from unittest.mock import MagicMock
from api.handlers.main_menu_handler import MainMenuHandler

from api.static.whats_iteration_messages import *
from api.static.state import *
from api.utils.user_info import build_user_info_message


class TestMainMenuHandler(unittest.TestCase):

    def setUp(self):
        # Mock database and Redis connections
        self.mock_db_connection = MagicMock()
        self.mock_redis_client = MagicMock()

        # Instantiate MainMenuHandler with mocked dependencies
        self.handler = MainMenuHandler(self.mock_db_connection, self.mock_redis_client)

        # Mock the persistence objects within the handler
        self.handler.user_persistence = MagicMock()
        self.handler.redis_persistence = MagicMock()

    def test_handle_main_message_invalid_input(self):
        """
        Test that an invalid message (non-integer) returns MAIN_MENU_OPTIONS.
        """
        message = "hello"
        sender = "user123"
        result = self.handler.handle_main_message(message, sender)
        self.assertEqual(result, MAIN_MENU_OPTIONS)
        self.handler.user_persistence.find_user.assert_not_called()
        self.handler.redis_persistence.set_state.assert_not_called()

    def test_handle_main_message_option_1_contact_us(self):
        """
        Test that message '1' returns CONTACT_US_MESSAGE.
        """
        message = "1"
        sender = "user123"
        result = self.handler.handle_main_message(message, sender)
        self.assertEqual(result, CONTACT_US_MESSAGE)
        self.handler.user_persistence.find_user.assert_not_called()
        self.handler.redis_persistence.set_state.assert_not_called()

    def test_handle_main_message_option_2_user_info_found(self):
        """
        Test that message '2' with a found user returns formatted user info.
        """
        message = "2"
        sender = "user123"
        mock_user = {"name": "John Doe", "email": "john@example.com"}
        self.handler.user_persistence.find_user.return_value = mock_user

        expected_message = build_user_info_message(mock_user)
        result = self.handler.handle_main_message(message, sender)
        self.assertEqual(result, expected_message)
        self.handler.user_persistence.find_user.assert_called_once_with(sender)
        self.handler.redis_persistence.set_state.assert_not_called()

    def test_handle_main_message_option_2_user_info_not_found(self):
        """
        Test that message '2' with no user found returns NO_USER_INFO_MESSAGE.
        """
        message = "2"
        sender = "user123"
        self.handler.user_persistence.find_user.return_value = None

        result = self.handler.handle_main_message(message, sender)
        self.assertEqual(result, NO_USER_INFO_MESSAGE)
        self.handler.user_persistence.find_user.assert_called_once_with(sender)
        self.handler.redis_persistence.set_state.assert_not_called()

    def test_handle_main_message_option_3_settings(self):
        """
        Test that message '3' sets the state in Redis and returns SETTINGS_OPTIONS.
        """
        message = "3"
        sender = "user123"
        result = self.handler.handle_main_message(message, sender)
        self.assertEqual(result, SETTINGS_OPTIONS)
        self.handler.redis_persistence.set_state.assert_called_once_with(
            key=sender,
            value=SETTINGS_STATE
        )
        self.handler.user_persistence.find_user.assert_not_called()

    def test_handle_main_message_unrecognized_option(self):
        """
        Test that an unrecognized integer option returns MAIN_MENU_OPTIONS.
        """
        message = "99"
        sender = "user123"
        result = self.handler.handle_main_message(message, sender)
        self.assertEqual(result, MAIN_MENU_OPTIONS)
        self.handler.user_persistence.find_user.assert_not_called()
        self.handler.redis_persistence.set_state.assert_not_called()


if __name__ == '__main__':
    unittest.main()