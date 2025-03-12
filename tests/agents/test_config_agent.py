import unittest
from unittest.mock import patch, MagicMock
from stage0_py_utils import Agent, create_config_agent

class TestConfigAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock bot agent."""
        self.mock_config = {}
        self.mock_bot = Agent("test_bot_agent")
        self.config_agent = create_config_agent(self.mock_bot)
        self.get_config = self.config_agent.actions["get_config"]["function"]

    @patch("stage0_py_utils.agents.config_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.config_agent.create_echo_breadcrumb")  
    @patch("stage0_py_utils.Config.to_dict")
    def test_get_configs_success(self, mock_config_to_dict, mock_create_breadcrumb, mock_create_token):
        """Test successful execution of get_configs action."""
       
        # Mock return values
        mock_create_token.return_value = "fake_token"
        mock_create_breadcrumb.return_value = "fake_breadcrumb"
        mock_config_to_dict.side_effect = Exception("Test Exception")
        
        # Call function
        arguments = ""
        result = self.get_config(arguments)
        
        # Assertions
        mock_create_token.assert_called_once()
        mock_create_breadcrumb.assert_called_once_with("fake_token")
        mock_config_to_dict.assert_called_once_with(token="fake_token")
        self.assertEqual(result, "error")
                    
if __name__ == "__main__":
    unittest.main()
