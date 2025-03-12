from copy import deepcopy
from datetime import datetime, timezone
import unittest
from unittest import TestLoader
from stage0_py_utils import Config, MongoIO
from pymongo import ASCENDING, DESCENDING

class TestMongoIO(unittest.TestCase):
    
    def setUp(self):
        self.config = Config.get_instance()
        self.test_id = "eeee00000000000000009999"
        self.test_collection_name = self.config.BOT_COLLECTION_NAME
        self.test_bot = {"status":"active","name":"Test","description":"A Test Bot","channels":[],"last_saved":{"fromIp":"","byUser":"","atTime":datetime(2025, 1, 1, 12, 34, 56),"correlationId":""}}
        self.document_created = False
        MongoIO._instance = None
        self.mongo_io = MongoIO.get_instance()

    def tearDown(self):
        if self.document_created:
            self.mongo_io.delete_document(self.test_collection_name, self.test_id)
        self.mongo_io.disconnect()
    
    def test_singleton_behavior(self):
        # Test that MongoIO is a singleton
        mongo_io1 = MongoIO.get_instance()
        mongo_io2 = MongoIO.get_instance()
        self.assertIs(mongo_io1, mongo_io2, "MongoIO should be a singleton")
        self.mongo_io.disconnect()

    def test_config_loaded(self):
        # Test that Config loaded version and enumerators
        self.assertIsInstance(self.config.versions, list)
        self.assertEqual(len(self.config.versions), 0)

        self.assertIsInstance(self.config.enumerators, dict)

    def test_CR_document(self):
        # Create a Test Document
        self.test_id = self.mongo_io.create_document(self.test_collection_name, self.test_bot)
        self.document_created = True
        id_str = str(self.test_id)
        
        self.assertEqual(id_str, str(self.test_id))

        # Retrieve the document
        document = self.mongo_io.get_document(self.test_collection_name, id_str)
        self.assertIsInstance(document, dict)
        self.assertEqual(document, self.test_bot)
        
    def test_CRU_document(self):
        # Create a Test Document
        self.test_id = self.mongo_io.create_document(self.test_collection_name, self.test_bot)
        self.document_created = True
        id_str = str(self.test_id)

        # Update the document with set data
        test_update = {"description": "A New test value"}
        document = self.mongo_io.update_document(self.test_collection_name, id_str, set_data=test_update)
        self.assertIsInstance(document, dict)
        self.assertEqual(document["description"], "A New test value")
        
    def test_add_to_set_document(self):
        # Create a Test Document
        self.test_id = self.mongo_io.create_document(self.test_collection_name, self.test_bot)
        self.document_created = True
        id_str = str(self.test_id)

        # Add a channel
        test_add_to_set = {"channels": "channel1"}
        document = self.mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 1)
        self.assertEqual(document["channels"][0], "channel1")

        # Re-Add a channel (should no-op)
        document = self.mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 1)
        self.assertEqual(document["channels"][0], "channel1")

        # Add another channel
        test_add_to_set = {"channels": "channel2"}
        document = self.mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 2)
        self.assertEqual(document["channels"][0], "channel1")
        self.assertEqual(document["channels"][1], "channel2")

    def test_push_document(self):
        # Create a Test Document
        self.test_id = self.mongo_io.create_document(self.test_collection_name, self.test_bot)
        self.document_created = True
        id_str = str(self.test_id)

        # Add a channel
        push_data = {"channels": "channel1"}
        document = self.mongo_io.update_document(self.test_collection_name, id_str, push_data=push_data)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 1)
        self.assertEqual(document["channels"][0], "channel1")

        # Re-Add a channel (should add duplicate)
        document = self.mongo_io.update_document(self.test_collection_name, id_str, push_data=push_data)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 2)
        self.assertEqual(document["channels"][0], "channel1")
        self.assertEqual(document["channels"][1], "channel1")

        # Add another channel
        test_add_to_set = {"channels": "channel2"}
        document = self.mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 3)
        self.assertEqual(document["channels"][0], "channel1")
        self.assertEqual(document["channels"][1], "channel1")
        self.assertEqual(document["channels"][2], "channel2")

    def test_pull_from_document(self):
        # Create a Test Document
        self.test_id = self.mongo_io.create_document(self.test_collection_name, self.test_bot)
        self.document_created = True
        id_str = str(self.test_id)

        # Add some channels
        test_add_to_set = {"channels": "channel1"}
        document = self.mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)
        test_add_to_set = {"channels": "channel2"}
        document = self.mongo_io.update_document(self.test_collection_name, id_str, add_to_set_data=test_add_to_set)

        # Remove channel1
        test_pull = {"channels": "channel1"}
        document = self.mongo_io.update_document(self.test_collection_name, id_str, pull_data=test_pull)
        self.assertIsInstance(document, dict)
        self.assertIsInstance(document["channels"], list)
        self.assertEqual(len(document["channels"]), 1)
        self.assertEqual(document["channels"][0], "channel2")
        
    def test_order_by_ASCENDING(self):
        match = {"currentVersion":"1.0.0.0"}
        project = {"collectionName": 1, "currentVersion": 1}
        order = [('collectionName', ASCENDING)]        
        
        result = self.mongo_io.get_documents(self.config.VERSION_COLLECTION_NAME, match, project, order)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["collectionName"], "bots")
        self.assertEqual(result[1]["collectionName"], "chains")
        self.assertEqual(result[2]["collectionName"], "conversations")
        self.assertEqual(result[3]["collectionName"], "exercises")
        self.assertEqual(result[4]["collectionName"], "workshops")

    def test_order_by_DESCENDING(self):
        match = {"currentVersion":"1.0.0.0"}
        project = {"collectionName": 1, "currentVersion": 1}
        order = [('collectionName', DESCENDING)]        
        
        result = self.mongo_io.get_documents(self.config.VERSION_COLLECTION_NAME, match, project, order)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[4]["collectionName"], "bots")
        self.assertEqual(result[3]["collectionName"], "chains")
        self.assertEqual(result[2]["collectionName"], "conversations")
        self.assertEqual(result[1]["collectionName"], "exercises")
        self.assertEqual(result[0]["collectionName"], "workshops")

    def test_get_all_full_documents(self):
        config = Config.get_instance()
        result = self.mongo_io.get_documents(config.VERSION_COLLECTION_NAME)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["collectionName"], "bots")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")

    def test_get_some_full_documents(self):
        config = Config.get_instance()
        match = {"collectionName":"chains"}
        result = self.mongo_io.get_documents(config.VERSION_COLLECTION_NAME, match)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["collectionName"], "chains")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")
        
    def test_get_all_partial_documents(self):
        config = Config.get_instance()
        project = {"_id":0, "collectionName":1, "currentVersion": 1}
        result = self.mongo_io.get_documents(config.VERSION_COLLECTION_NAME, project=project)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["collectionName"], "bots")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")
        self.assertNotIn("_id", result[0])
        
    def test_get_some_partial_documents(self):
        config = Config.get_instance()
        match = {"collectionName":"conversations"}
        project = {"_id":0, "collectionName":1, "currentVersion": 1}
        result = self.mongo_io.get_documents(config.VERSION_COLLECTION_NAME, match, project)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["collectionName"], "conversations")
        self.assertEqual(result[0]["currentVersion"], "1.0.0.0")
        self.assertNotIn("_id", result[0])

if __name__ == '__main__':
    unittest.main()