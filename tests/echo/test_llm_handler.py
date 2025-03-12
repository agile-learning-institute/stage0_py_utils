from datetime import datetime
import json
import unittest
from unittest.mock import MagicMock, patch

from bson import ObjectId
from stage0_py_utils import Message, LLMHandler

class TestLLMHandler(unittest.TestCase):
    def setUp(self):
        """Set up a mock LLMHandler instance before each test."""
        self.mock_handle_command = MagicMock()
        self.mock_llm_client = MagicMock()
        self.mock_llm_client.model = "test-model"
        self.llm_handler = LLMHandler(echo_bot_name="TEST_BOT", handle_command_function=self.mock_handle_command, llm_client=self.mock_llm_client)

    def test_stringify(self):
        """Make sure a simple raw string is returned quoted."""
        test_value = "this is a string"
        result = self.llm_handler.stringify(test_value)
        self.assertEqual(result, '"this is a string"')
        
    def test_stringify_object(self):
        """A object is returned with proper markup"""
        test_value = {"foo":"bar"}
        result = self.llm_handler.stringify(test_value)
        self.assertEqual(result, '{"foo":"bar"}')
        
    def test_stringify_list(self):
        """A list is returned with proper markup"""
        test_value = ["item1","item2"]
        result = self.llm_handler.stringify(test_value)
        self.assertEqual(result, '["item1","item2"]')
        
    def test_stringify_object_id(self):
        """A Mongo ObjectID values is returned as a string"""
        test_value = {"item1":ObjectId("123456789012345678901234")}
        result = self.llm_handler.stringify(test_value)
        self.assertEqual(result, '{"item1":"123456789012345678901234"}')
        
    def test_stringify_datetime(self):
        """A datetime value is returned as a string"""
        date_string = "2025-03-05 12:34:56.789000"
        test_value = {"item1":datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")}
        expected_value = '{"item1":"2025-03-05 12:34:56.789000"}'
        given_value = self.llm_handler.stringify(test_value)
        self.assertEqual(given_value, expected_value)
        
    def test_handle_simple_message(self):
        """Ensure simple agent call falls through."""
        # Arrange
        message1 = {"role": Message.USER_ROLE, "content": f"From:unknown To:{Message.GROUP_DIALOG} Simple Message"}
        message2 = {"role": Message.ASSISTANT_ROLE, "content": f"From:TEST_BOT To:{Message.GROUP_DIALOG} LLM Response"}
        message1_add = {"channel_id": "CHANNEL_1", "message": message1}
        message2_add = {"channel_id": "CHANNEL_1", "message": message2}
        llm_response = {"message": {"role": Message.ASSISTANT_ROLE, "content": f"From:TEST_BOT To:{Message.GROUP_DIALOG} LLM Response"}}
        
        self.mock_handle_command.side_effect = [
            [message1],
            [message1, message2]
        ]
        self.mock_llm_client.chat.return_value = llm_response

        # Act
        result = self.llm_handler.handle_message(channel="CHANNEL_1", text="Simple Message")

        # Assert
        self.assertEqual(result, "LLM Response")
        self.mock_llm_client.chat.assert_called_once()
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message1_add, separators=(',', ':'))}")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message2_add, separators=(',', ':'))}")

    def test_handle_message_with_agent_call(self):
        """Ensure user making agent call messages are correctly processed."""
        # Arrange
        agent_response = "Test Agent - Action Response"
        message1 = {"role": Message.USER_ROLE, "content": f"From:unknown To:{Message.GROUP_DIALOG} /test_agent/test_action"}
        message2 = {"role": Message.USER_ROLE, "content": f"From:test_agent To:{Message.GROUP_DIALOG} \"{agent_response}\""}
        message_add1 = {"channel_id": "CHANNEL_1", "message": message1}
        message_add2 = {"channel_id": "CHANNEL_1", "message": message2}
        
        self.mock_handle_command.side_effect = [
            [message1],
            agent_response,
            [message1, message2]
        ]

        # act
        result = self.llm_handler.handle_message(channel="CHANNEL_1", text="/test_agent/test_action")

        # assert
        self.assertEqual(result, '"Test Agent - Action Response"')
        self.mock_handle_command.assert_any_call("/test_agent/test_action")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message_add1, separators=(',', ':'))}")
        self.mock_handle_command.assert_any_call(f"/conversation/add_message/{json.dumps(message_add2, separators=(',', ':') )}")

    def test_handle_message_llm_agent_call(self):
        """Ensure llm can make 1 agent call"""
        # When LLM responds with a command, call the agent and interpret the response
        agent_reply = ["string1", "string2"]

        # Conversation
        text1 = "From:unknown To:group please execute the test command"
        text2 = "From:Echo To:tools /test_agent/test_command"
        text3 = "From:test_agent To:tools [\"string1\",\"string2\"]"
        text4 = "From:Echo To:group Looks like string1, and string2"

        message1 =             {"role": Message.USER_ROLE,      "content": text1}
        llm_rep1 = {"message": {"role": Message.ASSISTANT_ROLE, "content": text2}}
        message2 =             {"role": Message.ASSISTANT_ROLE, "content": text2}
        message3 =             {"role": Message.USER_ROLE,      "content": text3}
        llm_rep2 = {"message": {"role": Message.ASSISTANT_ROLE, "content": text4}}
        message4 =             {"role": Message.ASSISTANT_ROLE, "content": text4}
        
        message_add1 = f"/conversation/add_message/{json.dumps({"channel_id": "CHANNEL_1", "message":message1}, separators=(',', ':'))}"
        message_add2 = f"/conversation/add_message/{json.dumps({"channel_id": "CHANNEL_1", "message":message2}, separators=(',', ':'))}"
        message_add3 = f"/conversation/add_message/{json.dumps({"channel_id": "CHANNEL_1", "message":message3}, separators=(',', ':'))}"
        message_add4 = f"/conversation/add_message/{json.dumps({"channel_id": "CHANNEL_1", "message":message4}, separators=(',', ':'))}"

        self.mock_handle_command.side_effect = [
            [message1],
            [message1, message2],
            agent_reply,
            [message1, message2, message3],
            [message1, message2, message3, message4]
        ]
        self.mock_llm_client.chat.side_effect = [
            llm_rep1, llm_rep2
        ]

        # Act
        result = self.llm_handler.handle_message(channel="CHANNEL_1", text="please execute the test command")
        # Assert
        self.assertEqual(result, "Looks like string1, and string2")
        self.mock_handle_command.assert_any_call(message_add1)
        self.mock_handle_command.assert_any_call(message_add2)
        self.mock_handle_command.assert_any_call(message_add3)
        self.mock_handle_command.assert_any_call(message_add4)
        self.assertEqual(self.mock_llm_client.chat.call_count, 2)

    def test_handle_message_recursive_llm_agent_call(self):
        """Ensure llm can make multiple agent calls"""
        # When LLM responds with a command, call the agent and interpret the response
        agent_reply1 = ["string1", "string2"]
        agent_reply2 = {"foo": "bar"}

        # Conversation
        text1 = "From:mike To:group please execute the complex command" 
        text2 = "From:TEST_BOT To:tools /test_agent/test_command1"
        text3 = "From:test_agent To:tools [\"string1\",\"string2\"]"
        text4 = "From:TEST_BOT To:tools /test_agent/test_command2"
        text5 = "From:test_agent To:tools {\"foo\":\"bar\"}"
        text6 = "From:TEST_BOT To:group Looks like foo is bar"

        message1 =             {"role": Message.USER_ROLE,      "content": text1}
        llm_rep1 = {"message": {"role": Message.ASSISTANT_ROLE, "content": text2}}
        message2 =             {"role": Message.ASSISTANT_ROLE, "content": text2}
        message3 =             {"role": Message.USER_ROLE,      "content": text3}
        llm_rep2 = {"message": {"role": Message.ASSISTANT_ROLE, "content": text4}}
        message4 =             {"role": Message.ASSISTANT_ROLE, "content": text4}
        message5 =             {"role": Message.USER_ROLE,      "content": text5}
        llm_rep3 = {"message": {"role": Message.ASSISTANT_ROLE, "content": text6}}
        message6 =             {"role": Message.ASSISTANT_ROLE, "content": text6}
        
        message_add1 = f"/conversation/add_message/{json.dumps({"channel_id": "CHANNEL_1", "message":message1}, separators=(',', ':'))}"
        message_add2 = f"/conversation/add_message/{json.dumps({"channel_id": "CHANNEL_1", "message":message2}, separators=(',', ':'))}"
        message_add3 = f"/conversation/add_message/{json.dumps({"channel_id": "CHANNEL_1", "message":message3}, separators=(',', ':'))}"
        message_add4 = f"/conversation/add_message/{json.dumps({"channel_id": "CHANNEL_1", "message":message4}, separators=(',', ':'))}"
        message_add5 = f"/conversation/add_message/{json.dumps({"channel_id": "CHANNEL_1", "message":message5}, separators=(',', ':'))}"
        message_add6 = f"/conversation/add_message/{json.dumps({"channel_id": "CHANNEL_1", "message":message6}, separators=(',', ':'))}"

        self.mock_handle_command.side_effect = [
            [message1],
            [message1, message2],
            agent_reply1,
            [message1, message2, message3],
            [message1, message2, message3, message4],
            agent_reply2,
            [message1, message2, message3, message4, message5],
            [message1, message2, message3, message4, message5, message6]
        ]
        self.mock_llm_client.chat.side_effect = [
            llm_rep1, llm_rep2, llm_rep3
        ]

        # Act
        result = self.llm_handler.handle_message(channel="CHANNEL_1", text=text1)

        # Assert
        self.assertEqual(result, "Looks like foo is bar")
        self.mock_handle_command.assert_any_call(message_add1)
        self.mock_handle_command.assert_any_call(message_add2)
        self.mock_handle_command.assert_any_call(message_add3)
        self.mock_handle_command.assert_any_call(message_add4)
        self.mock_handle_command.assert_any_call(message_add5)
        self.mock_handle_command.assert_any_call(message_add6)
        self.assertEqual(self.mock_llm_client.chat.call_count, 3)

if __name__ == "__main__":
    unittest.main()

