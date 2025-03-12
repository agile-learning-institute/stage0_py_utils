import unittest
from unittest.mock import patch, MagicMock
from stage0_py_utils import ConversationServices

class TestConversationServices(unittest.TestCase):

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_get_conversations(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config_instance = MagicMock()
        mock_config_instance.LATEST_VERSION = "v1"
        mock_config_instance.ACTIVE_STATUS = "active"
        mock_config.return_value = mock_config_instance

        mock_mongo_instance.get_documents.return_value = [{"_id": "conv1", "channel_id": "CHANNEL_ID"}]

        token = {"user_id": "test_user"}
        result = ConversationServices.get_conversations(token)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["channel_id"], "CHANNEL_ID")

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_get_all_conversations_by_name(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()

        mock_mongo_instance.get_documents.return_value = [{"_id": "conv1", "channel_id": "CHANNEL_1"}]

        token = {"user_id": "test_user"}
        result = ConversationServices.get_all_conversations_by_name("Test", token)

        self.assertEqual(len(result), 1)
        self.assertIn("CHANNEL_1", [conv["channel_id"] for conv in result])

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_get_conversation(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()

        mock_mongo_instance.get_document.return_value = {"_id": "conv1", "channel_id": "CHANNEL_1"}

        token = {"user_id": "test_user"}
        result = ConversationServices.get_conversation("conv1", token)
        self.assertEqual(result["_id"], "conv1")

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_update_conversation(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()

        mock_mongo_instance.update_document.return_value = {"_id": "conv1", "updated": True}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        data = {"text": "Updated message"}

        result = ConversationServices.update_conversation("conv1", token, breadcrumb, data)
        self.assertEqual(result["updated"], True)

    @patch('stage0_py_utils.MongoIO.get_instance')
    @patch('stage0_py_utils.Config.get_instance')
    def test_add_message(self, mock_config, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_config.return_value = MagicMock()
        mock_update_return = {"_id": "conv1", "messages": "List Of Values"}
        mock_mongo_instance.update_document.return_value = mock_update_return

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        message = {"role":"user", "content": "New message"}

        result = ConversationServices.add_message(channel_id="conv1", message=message, token=token, breadcrumb=breadcrumb)
        self.assertEqual(result, mock_update_return["messages"])

if __name__ == '__main__':
    unittest.main()
