from flask import Blueprint, jsonify, request
from stage0_py_utils.echo.echo import Echo
from stage0_py_utils.flask_utils.token import create_flask_token
from stage0_py_utils.flask_utils.breadcrumb import create_flask_breadcrumb

import logging
logger = logging.getLogger(__name__)

# Define the Blueprint for config routes
def create_echo_routes(echo=None):
    echo_routes = Blueprint('echo_routes', __name__)
    if not isinstance(echo, Echo):
        raise Exception("create_echo_routes Error: an instance of Echo is a required parameter")
    
    # GET /api/echo - Return the agents
    @echo_routes.route('', methods=['GET'])
    def get_agents():
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            agents = echo.get_agents()
            logger.info(f"get_agents Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(agents), 200
        except Exception as e:
            logger.warning(f"get_agents {type(e)} exception has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/echo/agent/action - Return the agent action info
    @echo_routes.route('/<string:agent>/<string:action>', methods=['GET'])
    def get_action(agent, action):
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            action = echo.get_action(agent_name=agent, action_name=action)
            logger.info(f"get_action Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(action), 200
        except Exception as e:
            logger.warning(f"get_action {type(e)} exception has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/echo/message - Handle a message
    @echo_routes.route('/message', methods=['POST'])
    def handle_message():
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            message_data = request.get_json()
            response = echo.handle_message(message_data, token, breadcrumb)
            logger.info(f"handle_message Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(response), 200
        except Exception as e:
            logger.warning(f"handle_message {type(e)} exception has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    logger.info("Echo Flask Routes Registered")
    return echo_routes