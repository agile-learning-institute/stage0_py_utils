from flask import Blueprint, jsonify
from stage0_py_utils.config.config import Config
from stage0_py_utils.flask_utils.token import create_flask_token
from stage0_py_utils.flask_utils.breadcrumb import create_flask_breadcrumb

import logging
logger = logging.getLogger(__name__)

# Define the Blueprint for config routes
def create_config_routes():
    config_routes = Blueprint('config_routes', __name__)
    config = Config.get_instance()
    
    # GET /api/config - Return the current configuration as JSON
    @config_routes.route('', methods=['GET'])
    def get_config():
        try:
            # Return the JSON representation of the config object
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            logger.info(f"get_config Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(config.to_dict(token)), 200
        except Exception as e:
            logger.warning(f"get_config Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    logger.info("Config Flask Routes Registered")
    return config_routes