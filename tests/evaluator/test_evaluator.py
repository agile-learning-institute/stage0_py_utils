import unittest
from unittest.mock import patch, mock_open
from stage0_py_utils import Evaluator

class TestEvaluator(unittest.TestCase):

    def setUp(self):
        self.evaluator = Evaluator(
            name="TestEvaluator", 
            model="llama3.2:latest",
            grade_prompt_files=["grader1","grader2"],
            grade_prompt=[
                {"role":"user", "content":"Grade A Message"},
                {"role":"user", "content":"Watch for cheaters"},
                {"role":"user", "content":"Give a number"}
            ], 
            prompt_files=["prompt1","prompt2"],
            prompt=[
                {"role":"user", "content":"You are helpful"},
                {"role":"user", "content":"You are kind"},
                {"role":"user", "content":"You are supportive"},
            ], 
            conversations={
                "filename1.csv": [
                    {"role":"user", "content":"Message1"},
                    {"role":"assistant", "content":"Answer1"},
                    {"role":"user", "content":"Message2"},
                    {"role":"assistant", "content":"Answer2"},
                    {"role":"user", "content":"Message3"},
                    {"role":"assistant", "content":"Answer3"},
                    {"role":"user", "content":"Message4"},
                    {"role":"assistant", "content":"Answer4"}
                ],
                "filename2.csv": [
                    {"role":"user", "content":"Question 1"},
                    {"role":"assistant", "content":"Answer 1"},
                    {"role":"user", "content":"Question 2"},
                    {"role":"assistant", "content":"Answer 2"},
                    {"role":"user", "content":"Question 3"},
                    {"role":"assistant", "content":"Answer 3"},
                    {"role":"user", "content":"Question 4"},
                    {"role":"assistant", "content":"Answer 4"},
                    {"role":"user", "content":"Question 5"},
                    {"role":"assistant", "content":"Answer 5"},
                    {"role":"user", "content":"Question 6"},
                    {"role":"assistant", "content":"Answer 6"},
                ]
            }
        )

    def tearDown(self):
        pass
    
    def test_chat(self):
        # NOTE: Requires ollama, does not mock backing service
        # Arrange
        messages = [
            {"role":"system", "content":"You are nice"},
            {"role":"system", "content":"You are helpful"},
            {"role":"user", "content":"Hi"},
            {"role":"assistant", "content":"Hello, nice to meet you"},
        ]
        # Act
        message, latency = self.evaluator.chat(messages=messages)

        # Assert
        self.assertIsInstance(message, dict)
        self.assertEqual(message["role"], "assistant")
        self.assertIsInstance(message["content"], str)
        self.assertIsInstance(latency, int)

    @patch.object(Evaluator, 'chat')
    def test_grade_reply_valid_float(self, mock_chat):
        """Test grade_reply when LLM returns a valid float string."""
        # Arrange
        mock_chat.return_value = ({"content": "the grade is 0.85"}, 12345)
        messages = self.evaluator.grade_prompt[:]
        messages.append({"role":"user", "content": "Given:\nGreat Answer!\nExpected:\nGood Answer"})

        # Act
        grade = self.evaluator.grade_reply(expected="Good Answer", given="Great Answer!")

        # Assert        
        self.assertEqual(grade, 0.85)
        mock_chat.assert_called_with(model=None, messages=messages)

    @patch.object(Evaluator, 'chat')
    def test_grade_reply_invalid_float(self, mock_chat):
        """Test grade_reply when LLM returns an invalid float string."""
        # Arrange
        mock_chat.return_value = ({"content": "A low grade"}, 12345)

        # Act
        grade = self.evaluator.grade_reply(expected="Good Answer", given="Great Answer!")

        # Assert        
        self.assertIsNone(grade)

    @patch.object(Evaluator, 'grade_reply')
    @patch.object(Evaluator, 'chat')
    def test_grade_conversation(self, mock_chat, mock_grade_reply):
        # Arrange
        mock_grade_reply.side_effect = [1.0, 2.12, 3.14]
        mock_chat.side_effect = [
            ({"role":"assistant", "content":"Reply 1"}, 1234),
            ({"role":"assistant", "content":"Reply 2"}, 5678),
            ({"role":"assistant", "content":"Reply 3"}, 9012),
        ]
        messages = [
            {"role":"system", "content":"You are nice"},
            {"role":"system", "content":"You are helpful"},
            {"role":"user", "content":"Hi"},
            {"role":"assistant", "content":"Hello, nice to meet you"},
            {"role":"user", "content":"What can you help me with"},
            {"role":"assistant", "content":"I'm a chat assistant"},
            {"role":"user", "content":"Can you help me think"},
            {"role":"assistant", "content":"I can help you reason a problem"},
        ]
        expected = [
            {"expected":"Hello, nice to meet you", "given":"Reply 1", "latency":1234, "grade":1.0},
            {"expected":"I'm a chat assistant", "given":"Reply 2", "latency":5678, "grade":2.12},
            {"expected":"I can help you reason a problem", "given":"Reply 3", "latency":9012, "grade":3.14}
        ]
        
        # Act
        grades = self.evaluator.grade_conversation(conversation=messages)
        
        # Assert
        self.assertEqual(grades, expected)

    @patch.object(Evaluator, 'grade_conversation')
    def test_evaluate(self, mock_grade_conversation):
        # Arrange
        mock_grade_conversation.side_effect = [
            [{"grades_for": "file1"}],
            [{"grades_for": "file2"}]
        ]
        expected = {
            "filename1.csv": [{"grades_for": "file1"}],
            "filename2.csv": [{"grades_for": "file2"}]
        }
        
        # Act
        grades = self.evaluator.evaluate()
        
        # Assert
        self.assertCountEqual(grades, expected)

if __name__ == "__main__":
    unittest.main()