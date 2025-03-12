import unittest
from datetime import datetime, timezone
from bson import ObjectId
import uuid
from stage0_py_utils import create_echo_breadcrumb


class TestCreateBreadcrumb(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_create_echo_breadcrumb(self):
        mock_token = {"user_id": "507f191e810c19729de860ea"}

        breadcrumb = create_echo_breadcrumb(mock_token)

        self.assertIsInstance(breadcrumb['atTime'], datetime)
        self.assertEqual(breadcrumb['byUser'], "507f191e810c19729de860ea")
        self.assertEqual(breadcrumb['fromIp'], 'discord')
        self.assertIsNotNone(breadcrumb['correlationId'])

if __name__ == '__main__':
    unittest.main()