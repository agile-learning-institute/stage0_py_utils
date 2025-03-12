import unittest
from unittest.mock import patch, MagicMock
from stage0_py_utils import Echo, create_echo_agent

class TestEchoAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock echo instance and initialize the agent."""
        self.mock_echo = MagicMock(spec=Echo)
        self.echo_agent = create_echo_agent("test_echo_agent", self.mock_echo)
        self.get_agents = self.echo_agent.actions["get_agents"]["function"]

    @patch("stage0_py_utils.agents.echo_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.echo_agent.create_echo_breadcrumb")  
    def test_get_agents_success(self, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test successful execution of get_agents action."""
       
        # Mock return values
        mock_create_echo_token.return_value = "fake_token"
        mock_create_echo_breadcrumb.return_value = "fake_breadcrumb"
        self.mock_echo.get_agents.return_value = ["agent1", "agent2"]

        # Call function
        result = self.get_agents(arguments={})

        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_called_once_with("fake_token")
        self.mock_echo.get_agents.assert_called_once()
        self.assertEqual(result, ["agent1", "agent2"])

    @patch("stage0_py_utils.agents.echo_agent.create_echo_token")  
    @patch("stage0_py_utils.agents.echo_agent.create_echo_breadcrumb")  
    def test_get_agents_failure(self, mock_create_echo_breadcrumb, mock_create_echo_token):
        """Test that get_agents returns 'error' on exception."""
        
        # Mock return values
        mock_create_echo_token.side_effect = Exception("Token creation failed")
        
        # Call function
        result = self.get_agents(arguments={})

        # Assertions
        mock_create_echo_token.assert_called_once()
        mock_create_echo_breadcrumb.assert_not_called()  
        self.mock_echo.get_agents.assert_not_called()  
        self.assertEqual(result, "error")

if __name__ == "__main__":
    unittest.main()