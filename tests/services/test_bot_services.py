import unittest
from unittest.mock import MagicMock, patch, MagicMock
from stage0_py_utils import BotServices

class TestBotServices(unittest.IsolatedAsyncioTestCase):

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_get_bots(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()
        mock_mongo_instance.get_documents.return_value = [{"_id": "bot1", "name": "Test Bot", "description": "Test Desc"}]

        token = {"user_id": "test_user"}
        result = BotServices.get_bots("query", token)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Test Bot")

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_get_bot(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()
        mock_mongo_instance.get_document.return_value = {"_id": "bot1", "name": "Test Bot"}

        token = {"user_id": "test_user"}
        result = BotServices.get_bot("bot1", token)
        self.assertEqual(result["_id"], "bot1")

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_update_bot(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()
        mock_mongo_instance.update_document.return_value = {"_id": "bot1", "last_saved": "breadcrumb"}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        data = {"name": "Updated Bot"}

        result = BotServices.update_bot("bot1", token, breadcrumb, data)
        self.assertEqual(result["last_saved"], "breadcrumb")

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_get_channels(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()
        mock_mongo_instance.get_document.return_value = {"channels": ["channel1", "channel2"]}

        token = {"user_id": "test_user"}
        result = BotServices.get_channels("bot1", token)
        self.assertIn("channel1", result)

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_add_channel(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()
        mock_mongo_instance.update_document.return_value = {"channels": ["channel1", "channel2"]}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        result = BotServices.add_channel("bot1", token, breadcrumb, "channel2")
        self.assertIn("channel2", result)

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_remove_channel(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()
        mock_mongo_instance.update_document.return_value = {"channels": ["channel1"]}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        result = BotServices.remove_channel("bot1", token, breadcrumb, "channel2")
        self.assertNotIn("channel2", result)

if __name__ == '__main__':
    unittest.main()
