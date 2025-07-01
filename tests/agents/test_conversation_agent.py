import unittest
from unittest.mock import patch, MagicMock
from stage0_py_utils import Agent, create_conversation_agent

class TestConversationAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock bot agent."""
        self.mock_bot = Agent("test_bot_agent")
        self.mock_conversation = {}
        self.conversation_agent = create_conversation_agent(self.mock_bot)
        self.get_conversations = self.conversation_agent.actions["get_conversations"]["function"]
        self.get_conversation = self.conversation_agent.actions["get_conversation"]["function"]
        self.update_conversation = self.conversation_agent.actions["update_conversation"]["function"]
        self.add_message = self.conversation_agent.actions["add_message"]["function"]

    @patch("stage0_py_utils.agents.conversation_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_breadcrumb")  
    @patch("stage0_py_utils.ConversationServices.get_conversations")
    def test_get_conversations_success(self, mock_get_conversations, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of get_conversations action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        fake_breadcrumb = {"at_time":"sometime", "correlation_id":"correlation_ID"}
        mock_create_echo_breadcrumb.return_value = fake_breadcrumb
        mock_get_conversations.return_value = "conversations_list"
        
        # Call function
        arguments = ""
        result = self.get_conversations(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_conversations.assert_called_once_with(token="fake_token")
        self.assertEqual(result, "conversations_list")
    
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_breadcrumb")  
    @patch("stage0_py_utils.ConversationServices.get_conversations")
    def test_get_conversations_fail(self, mock_get_conversations, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failure case for get_conversations action."""
        
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        fake_breadcrumb = {"atTime":"sometime", "correlationId":"correlation_ID"}
        mock_create_echo_breadcrumb.return_value = fake_breadcrumb
        mock_get_conversations.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = ""
        result = self.get_conversations(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_conversations.assert_called_once_with(token="fake_token")
        self.assertEqual(result, "error")
        
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_breadcrumb")  
    @patch("stage0_py_utils.ConversationServices.get_conversation")
    def test_get_conversation_success(self, mock_get_conversation, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of get_conversations action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        fake_breadcrumb = {"at_time":"sometime", "correlation_id":"correlation_ID"}
        mock_create_echo_breadcrumb.return_value = fake_breadcrumb
        mock_get_conversation.return_value = "a_conversation"
        
        # Call function
        arguments = "channel_1"
        result = self.get_conversation(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_conversation.assert_called_once_with(channel_id=arguments, token="fake_token", breadcrumb=fake_breadcrumb)
        self.assertEqual(result, "a_conversation")
    
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_breadcrumb")  
    @patch("stage0_py_utils.ConversationServices.get_conversation")
    def test_get_conversation_fail(self, mock_get_conversation, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test failure case for get_conversations action."""
        
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        fake_breadcrumb = {"atTime":"sometime", "correlationId":"correlation_ID"}
        mock_create_echo_breadcrumb.return_value = fake_breadcrumb
        mock_get_conversation.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = "channel_1"
        result = self.get_conversation(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_get_conversation.assert_called_once_with(channel_id=arguments, token="fake_token", breadcrumb=fake_breadcrumb)
        self.assertEqual(result, "error")
                
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_breadcrumb")  
    @patch("stage0_py_utils.ConversationServices.update_conversation")
    def test_update_conversation_success(self, mock_update_conversation, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of update_conversation action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        fake_breadcrumb = {"at_time":"sometime", "correlation_id":"correlation_ID"}
        mock_create_echo_breadcrumb.return_value = fake_breadcrumb
        mock_update_conversation.return_value = "a_conversation"
        
        # Call function
        arguments = {
            "channel_id": "channel_1",
            "name": "conversation name"
        }
        result = self.update_conversation(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_update_conversation.assert_called_once_with(channel_id=arguments["channel_id"], conversation=arguments, token="fake_token", breadcrumb=fake_breadcrumb)
        self.assertEqual(result, "a_conversation")
    
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_breadcrumb")  
    @patch("stage0_py_utils.ConversationServices.update_conversation")
    def test_update_conversation_fail(self, mock_update_conversation, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of update_conversation action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        fake_breadcrumb = {"atTime":"sometime", "correlationId":"correlation_ID"}
        mock_create_echo_breadcrumb.return_value = fake_breadcrumb
        mock_update_conversation.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = {
            "channel_id": "channel_1",
            "name": "conversation name"
        }
        result = self.update_conversation(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_update_conversation.assert_called_once_with(channel_id=arguments["channel_id"], conversation=arguments, token="fake_token", breadcrumb=fake_breadcrumb)
        self.assertEqual(result, "error")
                
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_breadcrumb")  
    @patch("stage0_py_utils.ConversationServices.add_message")
    def test_add_message_success(self, mock_add_message, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of add_message action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        fake_breadcrumb = {"at_time":"sometime", "correlation_id":"correlation_ID"}
        mock_create_echo_breadcrumb.return_value = fake_breadcrumb
        mock_add_message.return_value = "array of messages"
        
        # Call function
        arguments = {
            "channel_id": "channel_1",
            "message": "This is a new message"
        }
        result = self.add_message(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_add_message.assert_called_once_with(channel_id=arguments["channel_id"], message=arguments["message"], token="fake_token", breadcrumb=fake_breadcrumb)
        self.assertEqual(result, "array of messages")
    
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.conversation_agent.create_echo_breadcrumb")  
    @patch("stage0_py_utils.ConversationServices.add_message")
    def test_add_message_fail(self, mock_add_message, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test fail of add_message action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        fake_breadcrumb = {"atTime":"sometime", "correlationId":"correlation_ID"}
        mock_create_echo_breadcrumb.return_value = fake_breadcrumb
        mock_add_message.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = {
            "channel_id": "channel_1",
            "message": "This is a new message"
        }
        result = self.add_message(arguments)
        
        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        mock_add_message.assert_called_once_with(channel_id=arguments["channel_id"], message=arguments["message"], token="fake_token", breadcrumb=fake_breadcrumb)
        self.assertEqual(result, "error")
                    
if __name__ == "__main__":
    unittest.main()
