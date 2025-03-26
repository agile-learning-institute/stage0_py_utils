import unittest
from unittest.mock import patch, MagicMock
from stage0_py_utils.echo.ollama_llm_client import OllamaLLMClient

class TestOllamaLLMClient(unittest.TestCase):

    @patch("stage0_py_utils.echo.ollama_llm_client.ollama.Client")
    def test_chat_returns_expected_response(self, MockOllamaClient):
        # Arrange: setup mock
        mock_instance = MockOllamaClient.return_value
        expected_response = {
            "message": {"role": "assistant", "content": "Hello!"},
            "total_duration": 1234
        }
        mock_instance.chat.return_value = expected_response

        # Act: call method under test
        client = OllamaLLMClient(model="test-model")
        messages = [{"role": "user", "content": "Hi"}]
        result = client.chat(messages=messages)

        # Assert
        self.assertEqual(result, expected_response)
        mock_instance.chat.assert_called_once_with(model="test-model", messages=messages)

if __name__ == "__main__":
    unittest.main()