import unittest
from datetime import datetime, timezone
import uuid
from flask import Flask
from stage0_py_utils import create_flask_breadcrumb


class TestCreateBreadcrumb(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_create_flask_breadcrumb(self):
        mock_token = {"user_id": "507f191e810c19729de860ea"}

        with self.app.test_request_context(
            '/some_endpoint',
            headers={'X-Correlation-Id': '123e4567-e89b-12d3-a456-426614174000'},
            environ_base={'REMOTE_ADDR': '192.168.1.1'}
        ):
            breadcrumb = create_flask_breadcrumb(mock_token)

            self.assertIsInstance(breadcrumb['atTime'], datetime)
            self.assertEqual(breadcrumb['byUser'], "507f191e810c19729de860ea")
            self.assertEqual(breadcrumb['fromIp'], '192.168.1.1')
            self.assertEqual(breadcrumb['correlationId'], '123e4567-e89b-12d3-a456-426614174000')

    def test_create_flask_breadcrumb_without_correlation_id(self):
        mock_token = {"user_id": "507f191e810c19729de860ea"}

        with self.app.test_request_context(
            '/another_endpoint',
            environ_base={'REMOTE_ADDR': '10.0.0.1'}
        ):
            breadcrumb = create_flask_breadcrumb(mock_token)

            self.assertIsInstance(breadcrumb['atTime'], datetime)
            self.assertEqual(breadcrumb['byUser'], "507f191e810c19729de860ea")
            self.assertEqual(breadcrumb['fromIp'], '10.0.0.1')
            self.assertIsInstance(uuid.UUID(breadcrumb['correlationId']), uuid.UUID)


if __name__ == '__main__':
    unittest.main()