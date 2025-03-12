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
            logger.debug(f"get_agents Success {breadcrumb}")
            agents = echo.get_agents()
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
            logger.debug(f"get_action Success {breadcrumb}")
            return jsonify(action), 200
        except Exception as e:
            logger.warning(f"get_action {type(e)} exception has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/echo/message/channel_id - Process a message to a conversation
    @echo_routes.route('/message/<string:channel_id>', methods=['POST'])
    def handle_message(channel_id):
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            arguments = request.get_json()
            action = echo.llm_handler.handle_message(channel=channel_id, user=arguments["user"], text=arguments["text"])
            logger.debug(f"handle_message Success {breadcrumb}")
            return jsonify(action), 200
        except Exception as e:
            logger.warning(f"handle_message {type(e)} exception has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    logger.info("Echo Flask Routes Registered")
    return echo_routes