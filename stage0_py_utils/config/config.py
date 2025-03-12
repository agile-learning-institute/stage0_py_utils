import os
import json
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

class Config:
    _instance = None  # Singleton instance

    def __init__(self):
        if Config._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Config._instance = self
            self.config_items = []
            self.versions = []
            self.enumerators = {}
            self.CONFIG_FOLDER = "./"
            
            # Declare instance variables to support IDE code assist
            self.BUILT_AT = ''
            self.CONFIG_FOLDER = ''
            self.LOGGING_LEVEL = ''
            self.LATEST_VERSION = ''
            self.ACTIVE_STATUS = ''
            self.ARCHIVED_STATUS = ''
            self.PENDING_STATUS = ''
            self.COMPLETED_STATUS = ''
            self.MONGO_DB_NAME = ''
            self.BOT_COLLECTION_NAME = ''
            self.CHAIN_COLLECTION_NAME = ''
            self.CONVERSATION_COLLECTION_NAME = ''
            self.WORKSHOP_COLLECTION_NAME = ''
            self.EXERCISE_COLLECTION_NAME = ''
            self.VERSION_COLLECTION_NAME = ''
            self.ELASTIC_INDEX_NAME = ''
            self.DISCORD_FRAN_TOKEN = ''
            self.STAGE0_FRAN_TOKEN = ''
            self.FRAN_MODEL_NAME = ''
            self.FRAN_API_PORT = 0
            self.FRAN_BOT_ID = ''
            self.SEARCH_API_PORT = 0
            self.MONGO_CONNECTION_STRING = ''
            self.ELASTIC_CLIENT_OPTIONS = {}
    
            # Default Values grouped by value type            
            self.config_strings = {
                "BUILT_AT": "LOCAL",
                "CONFIG_FOLDER": "./",
                "LOGGING_LEVEL": "INFO", 
                "LATEST_VERSION": "latest",
                "ACTIVE_STATUS": "active",
                "ARCHIVED_STATUS": "archived",
                "PENDING_STATUS": "pending",
                "COMPLETED_STATUS": "complete",
                "MONGO_DB_NAME": "stage0",
                "BOT_COLLECTION_NAME": "bots",
                "CHAIN_COLLECTION_NAME": "chains",
                "CONVERSATION_COLLECTION_NAME": "conversations",
                "WORKSHOP_COLLECTION_NAME": "workshops",
                "EXERCISE_COLLECTION_NAME": "exercises",
                "VERSION_COLLECTION_NAME": "msmCurrentVersions",
                "ELASTIC_INDEX_NAME": "stage0",
                "FRAN_MODEL_NAME": "Fran",
                "FRAN_BOT_ID": "BBB000000000000000000001",
            }
            self.config_ints = {
                "FRAN_API_PORT": "8580",
                "SEARCH_API_PORT": "8581",
            }
            self.config_string_secrets = {  
                "MONGO_CONNECTION_STRING": "mongodb://root:example@localhost:27017/?tls=false&directConnection=true",
                "STAGE0_FRAN_TOKEN": "BBB000000000000000000001",
                "DISCORD_FRAN_TOKEN": ""
            }
            self.config_json_secrets = {
                "ELASTIC_CLIENT_OPTIONS": '{"node":"http://localhost:9200"}',
            }

            # Initialize configuration
            self.initialize()

    def initialize(self):
        """Initialize configuration values."""
        self.config_items = []
        self.versions = []
        self.enumerators = {}

        # Initialize Config Strings
        for key, default in self.config_strings.items():
            value = self._get_config_value(key, default, False)
            setattr(self, key, value)
            
        # Initialize Config Integers
        for key, default in self.config_ints.items():
            value = int(self._get_config_value(key, default, False))
            setattr(self, key, value)
            
        # Initialize String Secrets
        for key, default in self.config_string_secrets.items():
            value = self._get_config_value(key, default, True)
            setattr(self, key, value)

        # Initialize JSON Secrets
        for key, default in self.config_json_secrets.items():
            value = json.loads(self._get_config_value(key, default, True))
            setattr(self, key, value)

        # Set Logging Level
        logging.basicConfig(level=self.LOGGING_LEVEL)
        logger.info(f"Configuration Initialized: {self.config_items}")
            
    def _get_config_value(self, name, default_value, is_secret):
        """Retrieve a configuration value, first from a file, then environment variable, then default."""
        value = default_value
        from_source = "default"

        # Check for config file first
        file_path = Path(self.CONFIG_FOLDER) / name
        if file_path.exists():
            value = file_path.read_text().strip()
            from_source = "file"
            
        # If no file, check for environment variable
        elif os.getenv(name):
            value = os.getenv(name)
            from_source = "environment"

        # Record the source of the config value
        self.config_items.append({
            "name": name,
            "value": "secret" if is_secret else value,
            "from": from_source
        })
        return value

    # Add a custom enumerator to the enumerators list
    def add_enumerator(self, enumerations):
        self.enumerators.update(enumerations)
        return
    
    # Serializer
    def to_dict(self, token):
        """Convert the Config object to a dictionary with the required fields."""
        return {
            "config_items": self.config_items,
            "versions": self.versions,
            "enumerators": self.enumerators,
            "token": token
        }    

    # Singleton Getter
    @staticmethod
    def get_instance():
        """Get the singleton instance of the Config class."""
        if Config._instance is None:
            Config()
            
        # logger.log("Config Initializing")
        return Config._instance
        