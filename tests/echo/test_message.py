import unittest
from stage0_py_utils import Message

class TestMessage(unittest.TestCase):

    def test_constructor_from_good_llm_message(self):
        """Test llm_message based constructor with valid message"""        
        test_text = f"From:flatballflyer-1052627280754647040 To:{Message.GROUP_DIALOG} Hi"
        message = Message(llm_message={"role":Message.USER_ROLE, "content":test_text})
        self.assertEqual(message.role, Message.USER_ROLE)
        self.assertEqual(message.user, "flatballflyer-1052627280754647040")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.text, "Hi")

    def test_constructor_from_bad_llm_message1(self):
        """Test llm_message based constructor with valid message"""        
        test_text = "To:Tools From:Someone Boo"
        message = Message(llm_message={"role":Message.ASSISTANT_ROLE, "content":test_text})
        self.assertEqual(message.role, Message.ASSISTANT_ROLE)
        self.assertEqual(message.user, "unknown")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.text, test_text)

    def test_constructor_from_bad_llm_message2(self):
        """Test llm_message based constructor with valid message"""        
        bad_text = "From:Mike To:Everyone Whats up"
        message = Message(llm_message={"role":Message.ASSISTANT_ROLE, "content":bad_text})
        self.assertEqual(message.role, Message.ASSISTANT_ROLE)
        self.assertEqual(message.user, "Mike")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.text, "Whats up")

    def test_constructor_from_good_encoded_text(self):
        """Test encoded text based constructor"""
        test_text = f"From:Mike To:{Message.GROUP_DIALOG} Hi"
        message = Message(encoded_text=test_text)
        self.assertEqual(message.role, Message.USER_ROLE)
        self.assertEqual(message.user, "Mike")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.text, "Hi")

    def test_constructor_from_good_encoded_text_with_role(self):
        """Test encoded text based constructor"""
        test_text = f"From:Fran To:{Message.TOOLS_DIALOG} Hi"
        message = Message(encoded_text=test_text, role=Message.ASSISTANT_ROLE)
        self.assertEqual(message.role, Message.ASSISTANT_ROLE)
        self.assertEqual(message.user, "Fran")
        self.assertEqual(message.dialog, Message.TOOLS_DIALOG)
        self.assertEqual(message.text, "Hi")

    def test_constructor_bad_encoded_text_with_role(self):
        """Test encoded text based constructor"""
        test_text = f"From:Fran To: {Message.TOOLS_DIALOG} Hi"
        message = Message(encoded_text=test_text, role=Message.ASSISTANT_ROLE)
        self.assertEqual(message.role, Message.ASSISTANT_ROLE)
        self.assertEqual(message.user, "Fran")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.text, "tools Hi")

    def test_constructor_bad_encoded_text_with_defaults(self):
        """Test encoded text based constructor"""
        test_text = "This is a bad message"
        message = Message(encoded_text=test_text, role=Message.ASSISTANT_ROLE, dialog=Message.TOOLS_DIALOG, user="test_user")
        self.assertEqual(message.role, Message.ASSISTANT_ROLE)
        self.assertEqual(message.user, "test_user")
        self.assertEqual(message.dialog, Message.TOOLS_DIALOG)
        self.assertEqual(message.text, test_text)

    def test_constructor_semi_bad_encoded_text_with_defaults(self):
        """Test encoded text based constructor"""
        test_text = "From:RealUser This is a bad message"
        message = Message(encoded_text=test_text, role=Message.ASSISTANT_ROLE, dialog=Message.TOOLS_DIALOG, user="test_user")
        self.assertEqual(message.role, Message.ASSISTANT_ROLE)
        self.assertEqual(message.user, "RealUser")
        self.assertEqual(message.dialog, Message.TOOLS_DIALOG)
        self.assertEqual(message.text, test_text)

    def test_constructor_good_encoded_text_with_defaults(self):
        """Test encoded text based constructor"""
        test_text = "From:RealUser To:group This is a good message"
        message = Message(encoded_text=test_text, role=Message.ASSISTANT_ROLE, dialog=Message.TOOLS_DIALOG, user="test_user")
        self.assertEqual(message.role, Message.ASSISTANT_ROLE)
        self.assertEqual(message.user, "RealUser")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.text, "This is a good message")

    def test_constructor_default(self):
        """Test message based constructor with message without a role"""
        message = Message()
        self.assertEqual(message.role, Message.USER_ROLE)
        self.assertEqual(message.user, "unknown")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.text, "")

    def test_constructor_with_text(self):
        """Test message based constructor with message without a role"""
        test_text = "Hello World!"
        message = Message(text=test_text)
        self.assertEqual(message.role, Message.USER_ROLE)
        self.assertEqual(message.user, "unknown")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.text, test_text)

    def test_constructor_with_text_and_role(self):
        """Test message based constructor with message without a role"""
        test_text = "Hello World!"
        message = Message(text=test_text, role=Message.ASSISTANT_ROLE)
        self.assertEqual(message.role, Message.ASSISTANT_ROLE)
        self.assertEqual(message.user, "unknown")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.text, test_text)

    def test_constructor_with_all_values(self):
        """Test message based constructor with message without a role"""
        test_text = "Hello World!"
        message = Message(user="Mike", role=Message.ASSISTANT_ROLE, dialog=Message.TOOLS_DIALOG, text=test_text)
        self.assertEqual(message.role, Message.ASSISTANT_ROLE)
        self.assertEqual(message.user, "Mike")
        self.assertEqual(message.dialog, Message.TOOLS_DIALOG)
        self.assertEqual(message.text, test_text)

    def test_constructor_for_route1(self):
        """Test message based constructor with plain"""
        test_text = "Hello World!"
        message = Message(encoded_text=test_text, user="Mike")
        self.assertEqual(message.role, Message.USER_ROLE)
        self.assertEqual(message.user, "Mike")
        self.assertEqual(message.dialog, Message.GROUP_DIALOG)
        self.assertEqual(message.text, test_text)
        
        llm_message = message.as_llm_message()
        self.assertEqual(llm_message["role"], Message.USER_ROLE)
        self.assertEqual(llm_message["content"], f"From:Mike To:{Message.GROUP_DIALOG} Hello World!")

    def test_as_LLM_Message(self):
        """Test the LLM Message projection """
        message = Message()
        expected_llm = {"role": Message.USER_ROLE, "content": f"From:unknown To:{Message.GROUP_DIALOG} "}
        given_llm = message.as_llm_message()
        self.assertEqual(expected_llm, given_llm)
        
    def test_as_dict(self):
        """Test the LLM Message projection """
        message = Message()
        expected = {
            "role": Message.USER_ROLE, 
            "user": "unknown",
            "dialog": Message.GROUP_DIALOG,
            "text": ""
        }
        given = message.as_dict()
        self.assertEqual(expected, given)

if __name__ == "__main__":
    unittest.main()