import json
import unittest
from datetime import datetime, timezone
from bson.objectid import ObjectId
from flask import Flask
from stage0_py_utils import MongoJSONEncoder  

class TestMongoJSONEncoder(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.json = MongoJSONEncoder(self.app)

    def test_encode_objectid(self):
        obj_id = ObjectId()
        result = self.app.json.dumps({'_id': obj_id})
        expected = f'{{"_id": "{str(obj_id)}"}}'
        self.assertEqual(result, expected)

    def test_encode_datetime(self):
        now = datetime.now(timezone.utc)
        result = self.app.json.dumps({'timestamp': now})
        expected = f'{{"timestamp": "{str(now)}"}}'
        self.assertEqual(result, expected)

    def test_encode_mixed_objects(self):
        obj_id = ObjectId()
        now = datetime.now(timezone.utc)
        data = {
            '_id': obj_id,
            'timestamp': now,
            'message': 'Test serialization'
        }
        result = self.app.json.dumps(data)
        expected = f'{{"_id": "{str(obj_id)}", "timestamp": "{str(now)}", "message": "Test serialization"}}'
        self.assertEqual(json.loads(result), json.loads(expected))

if __name__ == '__main__':
    unittest.main()