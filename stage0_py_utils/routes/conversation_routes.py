from stage0_py_utils.echo.message import Message
from stage0_py_utils.services.conversation_services import ConversationServices
from stage0_py_utils.flask_utils.breadcrumb import create_flask_breadcrumb
from stage0_py_utils.flask_utils.token import create_flask_token

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, Response, jsonify, request

# Define the Blueprint for conversation routes
def create_conversation_routes():
    conversation_routes = Blueprint('conversation_routes', __name__)

    # GET /api/conversations - Return a list of latest active conversations
    @conversation_routes.route('', methods=['GET'])
    def get_conversations():
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            conversations = ConversationServices.get_conversations(token=token)
            logger.info(f"get_conversations Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(conversations), 200
        except Exception as e:
            logger.warning(f"get_conversations Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # GET /api/conversation/channel_id - Return a specific conversation
    @conversation_routes.route('/<string:channel_id>', methods=['GET'])
    def get_conversation(channel_id):
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            conversation = ConversationServices.get_conversation(channel_id=channel_id, token=token, breadcrumb=breadcrumb)
            logger.info(f"get_conversation Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"get_conversation Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    # PUT /api/conversation/channel_id - Update a specific conversation
    @conversation_routes.route('/<string:channel_id>', methods=['PUT'])
    def update_conversation(channel_id):
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            data = request.get_json()
            conversation = ConversationServices.update_conversation(channel_id=channel_id, token=token, breadcrumb=breadcrumb, data=data)
            logger.info(f"update_conversation Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"update_conversation Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/conversation/channel_id/message - Add a message to a conversation
    @conversation_routes.route('/<string:channel_id>/message', methods=['POST'])
    def add_message(channel_id):
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            message_data = request.get_json()
            parsed_message = Message(llm_message=message_data, user=token["user_id"])
            messages = ConversationServices.add_message(channel_id=channel_id, message=parsed_message.as_llm_message(), token=token, breadcrumb=breadcrumb)
            logger.info(f"add_message Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(messages), 200
        except Exception as e:
            logger.warning(f"add_message Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # DELETE /api/conversation/channel_id - Reset a conversation
    @conversation_routes.route('/<string:channel_id>', methods=['DELETE'])
    def reset_conversation(channel_id):
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            conversation = ConversationServices.reset_conversation(channel_id=channel_id, token=token, breadcrumb=breadcrumb)
            logger.info(f"reset_conversation Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"reset_conversation Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/conversation/channel_id/load - Load a conversation from a file
    @conversation_routes.route('/<string:channel_id>/load', methods=['POST'])
    def load_conversation(channel_id):
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            data = request.get_json()
            conversation = ConversationServices.load_conversation(channel_id=channel_id, token=token, breadcrumb=breadcrumb, data=data)
            logger.info(f"load_conversation Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"load_conversation Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/conversation/channel_id/personality - Load a personality for a conversation
    @conversation_routes.route('/<string:channel_id>/personality', methods=['POST'])
    def load_personality(channel_id):
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            data = request.get_json()
            conversation = ConversationServices.load_personality(channel_id=channel_id, token=token, breadcrumb=breadcrumb, data=data)
            logger.info(f"load_personality Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"load_personality Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500
        
    # POST /api/conversation/initialize - Initialize a new conversation
    @conversation_routes.route('/initialize', methods=['POST'])
    def initialize_conversation():
        try:
            token = create_flask_token()
            breadcrumb = create_flask_breadcrumb(token)
            data = request.get_json()
            conversation = ConversationServices.initialize_conversation(token=token, breadcrumb=breadcrumb, data=data)
            logger.info(f"initialize_conversation Success {str(breadcrumb['at_time'])}, {breadcrumb['correlation_id']}")
            return jsonify(conversation), 200
        except Exception as e:
            logger.warning(f"initialize_conversation Error has occurred: {e}")
            return jsonify({"error": "A processing error occurred"}), 500

    logger.warning(f"TypeOf initialize_conversation {type(initialize_conversation)}")
    return conversation_routes