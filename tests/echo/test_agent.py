import unittest
from stage0_py_utils import Agent

class TestEchoAgent(unittest.TestCase):

    def setUp(self):
        """Initialize a test agent before each test."""
        self.agent = Agent("test_agent")

    def test_register_action_valid(self):
        """Ensure an action registers correctly with required attributes."""
        def sample_action(args):
            return "Executed"

        self.agent.register_action(
            action_name = "test_action",
            function = sample_action,
            description = "Test description",
            arguments_schema = {"type": "object", "properties": {}},
            output_schema = {"type": "string"}
        )

        self.assertIn("test_action", self.agent.get_actions())

    def test_register_action_missing_description(self):
        """Ensure registering an action without a description raises an error."""
        def sample_action(args):
            return "Executed"

        with self.assertRaises(ValueError) as context:
            self.agent.register_action(
                action_name="test_action",
                function=sample_action,
                description=None,  # Missing description
                arguments_schema={"type": "object", "properties": {}},
                output_schema={"type": "string"}
            )
        self.assertEqual(str(context.exception), "Missing required attributes for action registration")

    def test_register_action_missing_schemas(self):
        """Ensure registering an action without schemas raises an error."""
        def sample_action(args):
            return "Executed"

        with self.assertRaises(ValueError) as context:
            self.agent.register_action(
                action_name="test_action",
                function=sample_action,
                description="Test description",
                arguments_schema=None,  # Missing arguments_schema
                output_schema=None   # Missing output_schema
            )
        self.assertEqual(str(context.exception), "Missing required attributes for action registration")

    def test_invoke_registered_action(self):
        """Ensure invoking a registered action works."""
        def sample_action(args):
            return f"Received {args}"

        self.agent.register_action(
            action_name="test_action",
            function=sample_action,
            description="Test description",
            arguments_schema={"type": "object", "properties": {}},
            output_schema={"type": "string"}
        )

        result = self.agent.invoke_action("test_action", {"key": "value"})
        self.assertEqual(result, "Received {'key': 'value'}")

    def test_invoke_unregistered_action(self):
        """Ensure invoking an unregistered action returns an error."""
        result = self.agent.invoke_action("unknown_action", {})
        self.assertEqual(result, "Error: Action 'unknown_action' not found")

if __name__ == "__main__":
    unittest.main()