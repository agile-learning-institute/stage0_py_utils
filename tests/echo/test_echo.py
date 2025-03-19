import re
import unittest
import json
from stage0_py_utils import Agent, Echo
from unittest.mock import MagicMock, Mock, patch

import logging
logging.basicConfig(level="Debug")
logger = logging.getLogger(__name__)

class TestEcho(unittest.TestCase):

    def setUp(self):
        """Initialize Echo instance with Mock Agent before each test."""
        self.echo = Echo()
        
        self.mock_action = MagicMock()
        
        self.mock_agent = Agent("test_agent")
        self.mock_agent.register_action("test_action", self.mock_action, "description", "arguments_schema", "output_schema")
        self.echo.register_agent(agent=self.mock_agent)

    def test_register_agent(self):
        """Ensure an agent is registered successfully."""
        self.assertEqual(len(self.echo.get_agents()), 4)

    def test_register_invalid_agent(self):
        """Ensure registering a non-Agent instance raises an error."""
        with self.assertRaises(Exception):
            self.echo.register_agent("invalid_agent", "not_an_agent")

    def test_parse_command_valid(self):
        """Ensure a valid command is parsed correctly."""
        command = "/test_agent/test_action/{\"key\": \"value\"}"
        agent, action, arguments = self.echo.parse_command(command)

        self.assertEqual(agent, "test_agent")
        self.assertEqual(action, "test_action")
        self.assertEqual(arguments, {"key": "value"})

    def test_matcher1(self):
        command = "/test_agent/test_action/some text"
        match = Echo.ECHO_AGENT_COMMAND_PATTERN.match(command)
        
        self.assertIsNotNone(match, "Regex did not match the command")
        self.assertEqual(match.group(1), "test_agent")
        self.assertEqual(match.group(2), "test_action")
        self.assertEqual(match.group(3), "some text")
        
    def test_matcher2(self):
        command = "/test_agent/test_action/\"some text\""
        match = Echo.ECHO_AGENT_COMMAND_PATTERN.match(command)
        
        self.assertIsNotNone(match, "Regex did not match the command")
        self.assertEqual(match.group(1), "test_agent")
        self.assertEqual(match.group(2), "test_action")
        self.assertEqual(match.group(3), "\"some text\"")

    def test_matcher3(self):
        command = "/test_agent/test_action/some_text"
        match = Echo.ECHO_AGENT_COMMAND_PATTERN.match(command)
        
        self.assertIsNotNone(match, "Regex did not match the command")
        self.assertEqual(match.group(1), "test_agent")
        self.assertEqual(match.group(2), "test_action")
        self.assertEqual(match.group(3), "some_text")
        
    def test_matcher4(self):
        command = '/test_agent/test_action/{invalid_json}'
        match = Echo.ECHO_AGENT_COMMAND_PATTERN.match(command)
        
        self.assertIsNotNone(match, "Regex did not match the command")
        self.assertEqual(match.group(1), "test_agent")
        self.assertEqual(match.group(2), "test_action")
        self.assertEqual(match.group(3), "{invalid_json}")

    def test_matcher5(self):
        command = 'Your command syntax should be just \n/test_agent/test_action/arguments'
        match = Echo.ECHO_AGENT_COMMAND_PATTERN.match(command)
        
        self.assertIsNone(match)

    def test_parse_command_invalid_json(self):
        """Ensure command with invalid JSON raises an exception."""
        command = "/test_agent/test_action/some text"
        with self.assertRaises(Exception):
            self.echo.parse_command(command)
    
    @patch("stage0_py_utils.Agent.invoke_action")
    def test_handle_command_valid(self, mock_invoke_action):
        """Ensure a valid command is routed correctly."""
        command = "/test_agent/test_action/{\"key\": \"value\"}"
        mock_invoke_action.return_value = "Action executed successfully"
        result = self.echo.handle_command(command)
        
        self.assertEqual(result, "Action executed successfully")
        mock_invoke_action.assert_called_once_with("test_action", {"key": "value"})

    def test_handle_command_unknown_agent(self):
        """Ensure an unknown agent returns silence."""
        command = "/unknown_agent/test_action/{\"key\": \"value\"}"
        result = self.echo.handle_command(command)

        self.assertEqual(result[:50], "Unknown Agent unknown_agent. Available agents are:")

    def test_handle_command_unknown_action(self):
        """Ensure an unknown action returns available actions."""
        command = "/test_agent/unknown_action/{}"
        result = self.echo.handle_command(command)

        self.assertIn("Unknown action 'unknown_action'", result)
        self.assertIn("Available actions: test_action", result)

if __name__ == "__main__":
    unittest.main()
