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
            self.INPUT_FOLDER = ''
            self.OUTPUT_FOLDER = ''
            self.AUTO_PROCESS = False
            self.EXIT_AFTER_PROCESSING = False
            self.LOAD_TEST_DATA = False
            self.LOGGING_LEVEL = ''
            self.LATEST_VERSION = ''
            self.ACTIVE_STATUS = ''
            self.ARCHIVED_STATUS = ''
            self.PENDING_STATUS = ''
            self.COMPLETED_STATUS = ''
            self.MONGO_DB_NAME = ''
            self.OLLAMA_HOST = ''
            # New static collection names (singular, as used in the DB)
            self.BOT_COLLECTION_NAME = 'bot'
            self.CHAIN_COLLECTION_NAME = 'chain'
            self.CONVERSATION_COLLECTION_NAME = 'conversation'
            self.EXECUTION_COLLECTION_NAME = 'execution'
            self.EXERCISE_COLLECTION_NAME = 'exercise'
            self.RUNBOOK_COLLECTION_NAME = 'runbook'
            self.TEMPLATE_COLLECTION_NAME = 'template'
            self.USER_COLLECTION_NAME = 'user'
            self.WORKSHOP_COLLECTION_NAME = 'workshop'
            self.VERSION_COLLECTION_NAME = ''
            self.ELASTIC_INDEX_NAME = ''
            self.DISCORD_FRAN_TOKEN = ''
            self.STAGE0_FRAN_TOKEN = ''
            self.FRAN_MODEL_NAME = ''
            self.FRAN_BOT_PORT = 0
            self.FRAN_BOT_ID = ''
            self.SEARCH_API_PORT = 0
            self.MONGO_CONNECTION_STRING = ''
            self.ELASTIC_CLIENT_OPTIONS = {}
            # Search API specific configuration items
            self.ELASTIC_SEARCH_INDEX = ''
            self.ELASTIC_SYNC_INDEX = ''
            self.ELASTIC_SEARCH_MAPPING = {}
            self.ELASTIC_SYNC_MAPPING = {}
            self.ELASTIC_SYNC_PERIOD = 0
            self.SYNC_BATCH_SIZE = 0
            # Use the new static collection names for MONGO_COLLECTION_NAMES
            self.MONGO_COLLECTION_NAMES = [
                self.BOT_COLLECTION_NAME,
                self.CHAIN_COLLECTION_NAME,
                self.CONVERSATION_COLLECTION_NAME,
                self.EXECUTION_COLLECTION_NAME,
                self.EXERCISE_COLLECTION_NAME,
                self.RUNBOOK_COLLECTION_NAME,
                self.TEMPLATE_COLLECTION_NAME,
                self.USER_COLLECTION_NAME,
                self.WORKSHOP_COLLECTION_NAME
            ] 