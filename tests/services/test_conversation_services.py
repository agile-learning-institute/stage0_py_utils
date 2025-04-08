import unittest
from stage0_py_utils.config.config import Config
from unittest.mock import patch, MagicMock
from stage0_py_utils import ConversationServices
from stage0_py_utils.config.config import Config

class TestConversationServices(unittest.TestCase):
    
    @patch('stage0_py_utils.MongoIO.get_instance')
    def test_get_conversations(self, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance

        mock_mongo_instance.get_documents.return_value = [{"_id": "conv1", "channel_id": "CHANNEL_ID"}]

        token = {"user_id": "test_user"}
        result = ConversationServices.get_conversations(token=token)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["channel_id"], "CHANNEL_ID")

    @patch('stage0_py_utils.MongoIO.get_instance')
    def test_get_all_conversations_by_name(self, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance

        mock_mongo_instance.get_documents.return_value = [{"_id": "conv1", "channel_id": "CHANNEL_1"}]

        token = {"user_id": "test_user"}
        result = ConversationServices.get_all_conversations_by_name(query="Test", token=token)

        self.assertEqual(len(result), 1)
        self.assertIn("CHANNEL_1", [conv["channel_id"] for conv in result])

    @patch('stage0_py_utils.MongoIO.get_instance')
    def test_get_conversation(self, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_mongo_instance.get_document.return_value = {"_id": "conv1", "channel_id": "CHANNEL_1"}

        token = {"user_id": "test_user"}
        result = ConversationServices.get_conversation(channel_id="conv1", token=token)
        self.assertEqual(result["_id"], "conv1")

    @patch('stage0_py_utils.MongoIO.get_instance')
    def test_update_conversation(self, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance

        mock_mongo_instance.update_document.return_value = {"_id": "conv1", "updated": True}

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        data = {"text": "Updated message"}

        result = ConversationServices.update_conversation(
            channel_id="conv1", data=data,
            token=token, breadcrumb=breadcrumb
        )
        self.assertEqual(result["updated"], True)

    @patch('stage0_py_utils.MongoIO.get_instance')
    def test_add_message(self, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_update_return = {"_id": "conv1", "messages": "List Of Values"}
        mock_mongo_instance.update_document.return_value = mock_update_return

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        message = {"role":"user", "content": "New message"}

        result = ConversationServices.add_message(
            channel_id="conv1", message=message, 
            token=token, breadcrumb=breadcrumb
        )
        self.assertEqual(result, mock_update_return["messages"])

    @patch('stage0_py_utils.MongoIO.get_instance')
    def test_reset_conversation(self, mock_mongo):
        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_update_return = {"_id": "conv1", "messages": "List Of Values"}
        mock_mongo_instance.update_document.return_value = mock_update_return

        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}

        result = ConversationServices.reset_conversation(
            channel_id="conv1", token=token, breadcrumb=breadcrumb
        )
        
        mock_mongo_instance.update_document.assert_called_once()

    @patch('stage0_py_utils.services.conversation_services.ConversationServices.get_conversation')
    @patch('stage0_py_utils.services.conversation_services.MongoIO.get_instance')
    def test_load_named_conversation(self, mock_mongo_get, mock_get_conversation):
        # Setup Mocks
        config = Config.get_instance()
        mock_mongo = MagicMock()
        mock_mongo_get.return_value = mock_mongo
        fake_messages = [{"role": "user", "content": "Hello"}, {"role": "bot", "content": "Hi"}]
        mock_mongo.get_documents.return_value = [{"messages": fake_messages}]
        mock_get_conversation.return_value = {"channel_id": "conv1", "messages": []}

        updated_conversation = {
            "channel_id": "conv1",
            "messages": fake_messages,
            "last_saved": {"timestamp": "now"}
        }
        mock_mongo.update_document.return_value = updated_conversation

        # Run test
        token = {"user_id": "test_user"}
        breadcrumb = {"timestamp": "now"}
        result = ConversationServices.load_named_conversation(
            channel_id="conv1",
            named_conversation="from",
            token=token,
            breadcrumb=breadcrumb
        )

        # Assert outcomes
        mock_mongo.get_documents.assert_called_once_with(
            config.CONVERSATION_COLLECTION_NAME,
            match={"$and": [
                {"channel_id": "from"},
                {"version": config.LATEST_VERSION},
                {"status": config.ACTIVE_STATUS}
            ]}
        )

        mock_get_conversation.assert_called_once_with(
            channel_id="conv1",
            token=token,
            breadcrumb=breadcrumb
        )

        mock_mongo.update_document.assert_called_once_with(
            config.CONVERSATION_COLLECTION_NAME,
            match={"$and": [
                {"channel_id": "conv1"},
                {"version": config.LATEST_VERSION},
                {"status": config.ACTIVE_STATUS}
            ]},
            set_data={"last_saved": breadcrumb},
            push_data={"messages": {"$each": fake_messages}}
        )

        self.assertEqual(result, updated_conversation)
        
    @patch('stage0_py_utils.services.conversation_services.ConversationServices.get_conversation')
    @patch('stage0_py_utils.services.conversation_services.MongoIO.get_instance')
    def test_load_given_conversation(self, mock_mongo_get, mock_get_conversation):
        # Initialize Test Data
        csv_data = """role,from,to,text
user,alice,group,Hello Bob!
assistant,bob,group,Hi Alice!
user,alice,group,How are you today?
"""
        mock_conversation = {"foo":"bar"}
        mock_token = {"user_id": "test_user"}
        mock_breadcrumb = {"timestamp": "2025-03-12T10:00:00"}
        
        # Setup Mocks
        config = Config.get_instance()
        mock_mongo = MagicMock()
        mock_mongo_get.return_value = mock_mongo
        mock_get_conversation.return_value = mock_conversation
        mock_mongo.update_document.return_value = mock_conversation

        # Call the code
        result = ConversationServices.load_given_conversation(
            channel_id="workshop_001",
            csv_data=csv_data,
            token=mock_token,
            breadcrumb=mock_breadcrumb
        )

        # Assert Updates
        args, kwargs = mock_mongo.update_document.call_args
        pushed_messages = kwargs["push_data"]["messages"]["$each"]
        self.assertEqual(len(pushed_messages), 3)

        self.assertEqual(kwargs["match"], {
            "$and": [
                {"channel_id": "workshop_001"},
                {"version": config.LATEST_VERSION},
                {"status": config.ACTIVE_STATUS}
            ]
        })
        self.assertEqual(kwargs["set_data"], {"last_saved": mock_breadcrumb})

if __name__ == '__main__':
    unittest.main()
