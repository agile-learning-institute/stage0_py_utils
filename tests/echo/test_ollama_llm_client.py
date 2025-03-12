import unittest
from unittest.mock import patch, Mock
from stage0_py_utils import OllamaLLMClient

class TestOllamaLLMClient(unittest.TestCase):

    def setUp(self):
        """Initialize OllamaLLMClient before each test."""
        self.client = OllamaLLMClient()

    @patch('ollama.chat')
    def test_chat_success(self, mock_chat):
        """Ensure OllamaLLMClient successfully sends and receives messages."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.return_value = {"message": "Hello, world!"}
        mock_chat.return_value = mock_response

        messages = [{"role": "user", "content": "Hello"}]
        model_name = "llama3.2:latest"
        response = self.client.chat(model_name, messages)

        mock_chat.assert_called_once_with(model=model_name, messages=messages)
        self.assertEqual(response, mock_response)

    @patch('ollama.chat')
    def test_chat_failure(self, mock_chat):
        """Ensure OllamaLLMClient handles failed requests gracefully."""
        mock_chat.side_effect = Exception("Network error")

        messages = [{"role": "user", "content": "Hello"}]
        model_name = "llama3.2:latest"
        with self.assertRaises(Exception):
            self.client.chat(model_name, messages)

    def test_set_model(self):
        """Ensure setting a model updates the client correctly."""
        self.client.set_model("gemma")
        self.assertEqual(self.client.model, "gemma")

if __name__ == "__main__":
    unittest.main()
