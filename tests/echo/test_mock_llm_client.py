import unittest
from unittest.mock import patch
from stage0_py_utils import MockLLMClient  # Adjust import path as needed

class TestMockLLMClient(unittest.TestCase):
    
    def setUp(self):
        """Initialize MockLLMClient before each test."""
        self.client = MockLLMClient()

    def test_chat_returns_valid_reply(self):
        """Test that chat() returns a response from self.replies."""
        model = "test-model"
        messages = [{"from": "user", "to": "group", "content": "Hello"}]
        
        response = self.client.chat(messages=messages)

        self.assertIn(response, self.client.replies, "chat() returned an unexpected response")

    @patch("random.choice")
    def test_chat_uses_random_choice(self, mock_random_choice):
        """Test that random.choice() is called when selecting a reply."""
        mock_random_choice.return_value = "group:helpdesk staff need a lesson on what's funny and what's not."
        
        response = self.client.chat(messages=[])
        
        mock_random_choice.assert_called_once_with(self.client.replies)
        self.assertEqual(response, "group:helpdesk staff need a lesson on what's funny and what's not.")

if __name__ == "__main__":
    unittest.main()