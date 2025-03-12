# stage0_py_utils

This repo publishes the a pypl module that contains utility code used throughout the stage0 system.

## **Project Structure**

```text
📁 stage0_py_utils/                 # Repo root
│── 📁 stage0_py_utils/
│   │── 📁 agents/                    # Echo agent code
│   │   ├── bot_agents.py               # Agent for Echo Bot
│   │   ├── config_agents.py            # Agent for Config
│   │   ├── conversation_agents.py      # Agent for Echo Bot
│   │   ├── echo_agents.py              # Agent for Echo Bot
│   │
│   │── 📁 config/                         
│   │   ├── config.py                 # System Wide configuration utility
│   │
│   │── 📁 echo/                      # Multi-person LLM chat w/agents
│   │   ├── echo.py                     # Main Echo code, host to handle_command()
│   │   ├── agent.py                    # An Echo Agent with action() references
│   │   ├── discord_bot.py              # Discord on_message() @mention join/leave/etc.
│   │   ├── llm_handler.py              # LLM Chat manager handle_message()
│   │   ├── ollama_llm_client.py        # Ollama driver for LLM Handler
│   │   ├── mock_llm_client.py          # Static Reply driver for LLM Handler testing
│   │
│   │── 📁 echo_utils/                # Echo bot framework related utilities
│   │   ├── breadcrumb.py               # Create a breadcrumb with tracking information
│   │   ├── token.py                    # Decode a token for use in RBAC code
│   │
│   │── 📁 evaluator/                 # Echo bot framework evaluation utility
│   │   ├── evaluator.py                # Evaluation Engine
│   │   ├── loader.py                   # Loader to load evaluation csv files
│   │
│   │── 📁 flask_utils/               # Flask related utilities
│   │   ├── breadcrumb.py               # Create a breadcrumb with tracking information
│   │   ├── token.py                    # Decode a token for use in RBAC code
│   │   ├── ejson_encoder.py            # Encoder for rendering bson types to json
│   │
│   │── 📁 mongo_utils/               # MongoDB Utilities
│   │   ├── mongo_io.py                 # Simple wrapper for Mongo Document CRUD actions
│   │   ├── encode_properties.py        # Utility to encode json to mongo bson types
│   │
│   │── 📁 routes/                    # Flask Routes
│   │   ├── bot.py                      # Chat bot endpoints
│   │   ├── config.py                   # Config endpoints
│   │   ├── conversation.py             # Conversation endpoints
│   │   ├── echo.py                     # Echo endpoints
│   │
│   │── 📁 services/                  # Business Service Level implementation
│       ├── bot.py                      # Chat bot IO
│       ├── conversation.py             # Conversation IO
│   
│── 📁 test_data/                     # Testing Data
│   │── 📁 config/                      # Config testing data for config files
│   │── 📁 evaluate/                    # Echo Evaluate test data
│   
│── 📁 tests/                         # unittest code
│   │── 📁 agents/                       
│   │── 📁 echo/                         
│   │── 📁 echo_utils/                   
│   │── ....
│   
│── Pipfile
│── README.md
│── pyproject.toml
│── setup.cfg
│── ...
```

__all__ = [
    # Configuration and Database Utilities
    Config, create_config_agent, create_config_routes,
    MongoIO, EJSONEncoder, encode_document,

    # Echo Framework
    Echo, Agent, Message, DiscordBot, LLMHandler, MockLLMClient, OllamaLLMClient,
    create_echo_agent, create_echo_routes,
    BotServices, create_bot_agent, create_bot_routes, 
    ConversationServices, create_conversation_agent, create_conversation_routes,
    
    # Echo Utility Functions
    create_echo_breadcrumb, create_echo_token,

    # Flask Utility Functions
    create_flask_breadcrumb, create_flask_token,
    
    # LLM Model and Prompt Evaluator
    Evaluator, Loader,
]