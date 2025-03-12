import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from stage0_py_utils import create_config_routes

class TestConfigRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and app context."""
        self.app = Flask(__name__)
        self.app.register_blueprint(create_config_routes(), url_prefix='/api/config')
        self.client = self.app.test_client()

    @patch('stage0_py_utils.create_flask_token')
    @patch('stage0_py_utils.create_flask_breadcrumb')
    def test_get_config_success(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/config for successful response."""
        # Arrange
        mock_token = {"user_id": "mock_user"}
        mock_create_token.return_value = mock_token
        mock_breadcrumb = {"breadcrumb": "mock_breadcrumb"}
        mock_create_breadcrumb.return_value = mock_breadcrumb

        # Act
        response = self.client.get('/api/config')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json["config_items"], list)
        self.assertIsInstance(response.json["versions"], list)
        self.assertIsInstance(response.json["enumerators"], dict)
        
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with(mock_token)

    @patch('stage0_py_utils.create_flask_token')
    @patch('stage0_py_utils.create_flask_breadcrumb')
    def test_get_config_failure(self, mock_create_breadcrumb, mock_create_token):
        """Test GET /api/config when an exception is raised."""
        mock_create_token.side_effect = Exception("Token error")
        mock_create_breadcrumb.return_value = {"breadcrumb": "mock_breadcrumb"}

        response = self.client.get('/api/config')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

if __name__ == '__main__':
    unittest.main()
