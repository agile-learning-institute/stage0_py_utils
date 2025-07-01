import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from stage0_py_utils import Echo, create_echo_routes

class TestEchoRoutes(unittest.TestCase):
    
    def setUp(self):
        """Set up the Flask test client and mock Echo instance."""
        self.mock_echo = MagicMock(spec=Echo)

        self.app = Flask(__name__)
        self.app.register_blueprint(create_echo_routes(self.mock_echo), url_prefix='/api/echo')
        self.client = self.app.test_client()

    @patch('stage0_py_utils.routes.echo_routes.create_flask_token')
    @patch('stage0_py_utils.routes.echo_routes.create_flask_breadcrumb')
    def test_get_agents_success(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/echo when an exception occurs."""
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}

        response = self.client.get('/api/echo')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once()
        self.mock_echo.get_agents.assert_called_once()

    @patch('stage0_py_utils.routes.echo_routes.create_flask_token')
    @patch('stage0_py_utils.routes.echo_routes.create_flask_breadcrumb')
    def test_get_agents_failure(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/echo when an exception occurs."""
        mock_create_token.side_effect = Exception("Token error")
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}

        response = self.client.get('/api/echo')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_not_called()
        self.mock_echo.get_agents.assert_not_called()

    @patch('stage0_py_utils.routes.echo_routes.create_flask_token')
    @patch('stage0_py_utils.routes.echo_routes.create_flask_breadcrumb')
    def test_get_action_success(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/echo/{agent}/{action} for successful response."""
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        fake_breadcrumb = {"at_time":"sometime", "correlation_id":"correlation_ID"}
        mock_create_breadcrumb.return_value = fake_breadcrumb

        self.mock_echo.get_action.return_value = {"foo":"bar"}

        response = self.client.get('/api/echo/echo/get_agents')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"foo":"bar"})
        
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)
        self.mock_echo.get_action.assert_called_once()

    @patch('stage0_py_utils.routes.echo_routes.create_flask_token')
    @patch('stage0_py_utils.routes.echo_routes.create_flask_breadcrumb')
    def test_get_action_failure(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/echo/<name>/<name> when an exception occurs."""
        mock_create_token.return_value = {"user_id": "mock_user"}
        fake_breadcrumb = {"at_time":"sometime", "correlation_id":"correlation_ID"}
        mock_create_breadcrumb.return_value = fake_breadcrumb

        self.mock_echo.get_action.side_effect = Exception("Database error")

        response = self.client.get('/api/echo/agent1/action1')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with({"user_id": "mock_user"})
        self.mock_echo.get_action.assert_called_once_with(agent_name="agent1", action_name="action1")

if __name__ == '__main__':
    unittest.main()