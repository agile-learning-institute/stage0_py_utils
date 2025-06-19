from copy import deepcopy
from datetime import datetime, timezone
import unittest
from unittest import TestLoader
from stage0_py_utils import Config, MongoIO
from pymongo import ASCENDING, DESCENDING
from unittest.mock import patch

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
        try:
            self.mongo_io.delete_documents(self.config.VERSION_COLLECTION_NAME, {"collectionName": "test_upsert"})
            self.mongo_io.delete_document(self.test_collection_name, self.test_id)
            self.mongo_io.drop_collection("test_collection")
        except Exception as e:
            pass
        finally:
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

    def test_upsert_document(self):
        # Test upsert with new document
        match = {"collectionName": "test_upsert"}
        data = {"currentVersion": "test_version"}
        document = self.mongo_io.upsert_document(self.config.VERSION_COLLECTION_NAME, match, data)
        self.assertIsInstance(document, dict)
        self.assertEqual(document["collectionName"], "test_upsert")
        self.assertEqual(document["currentVersion"], "test_version")

        # Test upsert with existing document
        data = {"currentVersion": "updated_version"}
        document = self.mongo_io.upsert_document(self.config.VERSION_COLLECTION_NAME, match, data)
        self.assertIsInstance(document, dict)
        self.assertEqual(document["collectionName"], "test_upsert")
        self.assertEqual(document["currentVersion"], "updated_version")

    def test_schema_operations(self):
        # Test schema application
        schema = {
            "bsonType": "object",
            "required": ["name", "status"],
            "properties": {
                "name": {"bsonType": "string"},
                "status": {"bsonType": "string"}
            }
        }
        self.mongo_io.apply_schema("test_collection", schema)
        
        # Verify schema was applied
        validation_rules = self.mongo_io.get_schema("test_collection")
        self.assertIn("$jsonSchema", validation_rules)
        self.assertEqual(validation_rules["$jsonSchema"], schema)

        # Test schema removal
        self.mongo_io.remove_schema("test_collection")
        
        # Verify schema was removed
        validation_rules = self.mongo_io.get_schema("test_collection")
        self.assertEqual(validation_rules, {})

    def test_index_operations(self):
        # Test index creation
        new_indexes = [
            {
                "name": "test_index",
                "key": [("name", ASCENDING)]
            }
        ]
        self.mongo_io.create_index(self.test_collection_name, new_indexes)
        
        # Verify index was created
        indexes = self.mongo_io.get_indexes(self.test_collection_name)
        index_names = [idx["name"] for idx in indexes]
        self.assertIn("test_index", index_names)

        # Test index dropping
        self.mongo_io.drop_index(self.test_collection_name, "test_index")
        
        # Verify index was dropped
        indexes = self.mongo_io.get_indexes(self.test_collection_name)
        index_names = [idx["name"] for idx in indexes]
        self.assertNotIn("test_index", index_names)

    def test_pipeline_execution(self):
        # Create test documents
        test_docs = [
            {"name": "Test1", "status": "active"},
            {"name": "Test2", "status": "active"},
            {"name": "Test3", "status": "inactive"}
        ]
        for doc in test_docs:
            self.mongo_io.create_document("test_collection", doc)

        # Test pipeline execution
        pipeline = [
            {"$set": {"status": "archived"}},
            {"$out": "test_collection"}  
        ]
        self.mongo_io.execute_pipeline("test_collection", pipeline)
        
        # Verify pipeline execution
        documents = self.mongo_io.get_documents("test_collection", {})
        self.assertEqual(len(documents), 3)
        self.assertEqual(documents[0]["status"], "archived")
        self.assertEqual(documents[1]["status"], "archived")
        self.assertEqual(documents[2]["status"], "archived")

    def test_delete_document(self):
        # Create a test document
        self.mongo_io.get_collection("test_collection")
        self.test_id = self.mongo_io.create_document("test_collection", self.test_bot)

        # Delete by ID
        deleted_count = self.mongo_io.delete_document("test_collection", self.test_id)
        self.assertEqual(deleted_count, 1)
        self.document_created = False

    def test_delete_documents(self):
        # Create multiple test documents
        doc1 = {"name": "test1", "value": 1}
        doc2 = {"name": "test2", "value": 2}
        doc3 = {"name": "test3", "value": 3}
        
        self.mongo_io.create_document("test_collection", doc1)
        self.mongo_io.create_document("test_collection", doc2)
        self.mongo_io.create_document("test_collection", doc3)
        
        # Delete documents with match criteria
        deleted_count = self.mongo_io.delete_documents("test_collection", {"value": {"$lt": 3}})
        self.assertEqual(deleted_count, 2)
        
        # Verify remaining document
        remaining = self.mongo_io.get_documents("test_collection")
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0]["name"], "test3")

    def test_load_test_data_success_return_value(self):
        """Test that load_test_data returns proper success information."""
        import tempfile
        import os
        
        # Create a temporary JSON file with valid data
        test_data = [
            {
                "_id": {"$oid": "A00000000000000000000001"},
                "name": "test_document",
                "status": "active"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            import json
            json.dump(test_data, f)
            temp_file = f.name
        
        try:
            # Load the test data
            result = self.mongo_io.load_test_data("test_collection", temp_file)
            
            # Verify the return value structure
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["operation"], "load_test_data")
            self.assertEqual(result["collection"], "test_collection")
            self.assertEqual(result["documents_loaded"], 1)
            self.assertIsInstance(result["inserted_ids"], list)
            self.assertEqual(len(result["inserted_ids"]), 1)
            self.assertTrue(result["acknowledged"])
            
        finally:
            # Clean up
            os.unlink(temp_file)
            self.mongo_io.drop_collection("test_collection")

if __name__ == '__main__':
    unittest.main()