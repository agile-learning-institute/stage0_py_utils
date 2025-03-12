import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from stage0_py_utils import create_bot_routes, MongoJSONEncoder

class TestBotRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and app context."""
        self.app = Flask(__name__)
        self.app.json = MongoJSONEncoder(self.app)
        self.app.register_blueprint(create_bot_routes(), url_prefix='/api/bot')
        self.client = self.app.test_client()

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.get_bots')
    def test_get_bots_success(self, mock_get_bots, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/bot for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_bots.return_value = [{"id": "bot1", "name": "Test Bot"}]

        # Act
        response = self.client.get('/api/bot')

        # Assert
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_bots.assert_called_once_with("", mock_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"id": "bot1", "name": "Test Bot"}])

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.get_bots')
    def test_get_bots_failure(self, mock_get_bots, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/bot when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_bots.side_effect = Exception("Database error")

        response = self.client.get('/api/bot')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.get_bot')
    def test_get_bot_success(self, mock_get_bot, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/bot/{id} for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_bot.return_value = {"id": "bot1", "name": "Test Bot"}

        # Act
        response = self.client.get('/api/bot/bot1')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": "bot1", "name": "Test Bot"})
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_bot.assert_called_once_with("bot1", mock_token)

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.get_bot')
    def test_get_bot_failure(self, mock_get_bot, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/bot/{id} when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_bot.side_effect = Exception("Database error")

        response = self.client.get('/api/bot/bot1')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.update_bot', new_callable=MagicMock)
    def test_update_bot_success(self, mock_update_bot, mock_create_breadcrumb, mock_create_token):
        """Test PATCH /api/bot/{id} for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        mock_bot = {"id": "bot1", "foo": "bar"}
        mock_update_bot.return_value = mock_bot
        patch_data = {"foo": "bar"}

        # Act
        response = self.client.patch('/api/bot/bot1', json=patch_data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_bot)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_update_bot.assert_called_once_with("bot1", mock_token, mock_breadcrumb, patch_data)

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.update_bot', new_callable=MagicMock)
    def test_update_bot_failure(self, mock_update_bot, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/bots when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_update_bot.side_effect = Exception("Database error")

        response = self.client.patch('/api/bot/bot1', json={})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.get_channels')
    def test_get_channels_success(self, mock_get_channels, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/bot/{id}/channels for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        channels = ["channel1", "channel2", "channel3"]
        mock_get_channels.return_value = channels

        # Act
        response = self.client.get('/api/bot/bot1/channels')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, channels)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_get_channels.assert_called_once_with("bot1", mock_breadcrumb)

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.get_channels')
    def test_get_channels_failure(self, mock_get_channels, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/bot when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_get_channels.side_effect = Exception("Database error")

        response = self.client.get('/api/bot/bot1/channels')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.add_channel')
    def test_add_channel_success(self, mock_add_channel, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/bot/{id}/channel/{channel_id} for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        channels = ["channel1", "channel2", "channel3", "channel4"]
        mock_add_channel.return_value = channels

        # Act
        response = self.client.post('/api/bot/bot1/channel/channel4')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, channels)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_add_channel.assert_called_once_with("bot1", mock_token, mock_breadcrumb, "channel4")

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.add_channel')
    def test_add_channel_failure(self, mock_add_channel, mock_create_breadcrumb, mock_create_token):
        """Test POST /api/bot/{id}/channel/{channel_id} when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_add_channel.side_effect = Exception("Database error")

        response = self.client.post('/api/bot/bot1/channel/channel4')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.remove_channel')
    def test_remove_channel_success(self, mock_remove_channel, mock_create_breadcrumb, mock_create_token):
        """Test DELETE /api/bot/{id}/channel/{channel_id} for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb
        channels = ["channel1", "channel2", "channel3"]
        mock_remove_channel.return_value = channels

        # Act
        response = self.client.delete('/api/bot/bot1/channel/channel4')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, channels)
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        mock_remove_channel.assert_called_once_with("bot1", mock_token, mock_breadcrumb, "channel4")

    @patch('stage0_py_utils.routes.bot_routes.create_flask_token')
    @patch('stage0_py_utils.routes.bot_routes.create_flask_breadcrumb')
    @patch('stage0_py_utils.services.bot_services.BotServices.remove_channel')
    def test_remove_channel_failure(self, mock_remove_channel, mock_create_breadcrumb, mock_create_token):
        """Test DELETE /api/bot/{id}/channel/{channel_id} when an exception is raised."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}
        mock_remove_channel.side_effect = Exception("Database error")

        response = self.client.delete('/api/bot/bot1/channel/channel4')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

if __name__ == '__main__':
    unittest.main()