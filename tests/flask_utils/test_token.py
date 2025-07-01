import unittest
from stage0_py_utils import create_flask_token 


class TestCreateToken(unittest.TestCase):
    def test_create_token(self):
        token = create_flask_token()
        
        # Expected token structure
        expected = {
            "user_id": "aaaa00000000000000000001",
            "roles": ["Staff", "admin"]
        }

        self.assertEqual(token, expected)


if __name__ == '__main__':
    unittest.main()