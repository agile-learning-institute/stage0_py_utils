# stage0_py_utils

This repo publishes the a pypl module that contains utility code used throughout the stage0 system. See the [ECHO](./ECHO.md) documentation for information on how the [Stage0 Echo Bot](https://github.com/agile-learning-institute/stage0/blob/main/ECHO.md) is implemented. 

## Importable components

### Configuration and Database Utilities
Config, create_config_agent, create_config_routes,
MongoIO, EJSONEncoder, encode_document,

---

### Echo Framework
Echo, Agent, Message, DiscordBot, LLMHandler, MockLLMClient, OllamaLLMClient,
create_echo_agent, create_echo_routes,
BotServices, create_bot_agent, create_bot_routes, 
ConversationServices, create_conversation_agent, create_conversation_routes,

---

### Echo Utility Functions
create_echo_breadcrumb, create_echo_token,

---

### Flask Utility Functions
create_flask_breadcrumb, create_flask_token,

---

### LLM Model and Prompt Evaluator
Evaluator, Loader,

# Contributing

## Prerequisites

- [Stage0 Developer Edition]() #TODO for now Docker
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

### Optional

- [Mongo Compass](https://www.mongodb.com/try/download/compass) - if you want a way to look into the database

## Folder structure for source code

```text
📁 stage0_py_utils/                 # Repo root
│── 📁 stage0_py_utils/
│   │── 📁 agents/                 # Echo agent implementations
│   │── 📁 config/                 # System Wide configuration
│   │── 📁 echo/                   # Echo Chat AI Framework
│   │── 📁 echo_utils/             # Echo related utilities
│   │── 📁 flask_utils/            # Flask related utilities
│   │── 📁 mongo_utils/            # MongoDB Utilities
│   │── 📁 evaluator/              # Echo evaluation utility
│   │── 📁 routes/                 # Flask Routes
│   │── 📁 services/               # Persistence Services
│   
│── 📁 test_data/                  # Testing Data
│   │── 📁 config/                   # Config file testing data
│   │── 📁 evaluate/                 # Echo Evaluate test data
│   
│── 📁 tests/                      # unittest code
│   │── 📁 agents/                       
│   │── 📁 echo/                         
│   │── 📁 echo_utils/                   
│   │── ....
│   
│── README.md
│── ...
```

---

## Install Dependencies

```bash
pipenv install
```

## Run Unit Testing

```bash
pipenv run test
```
NOTE: The test of the MongoIO class expect to find a running stage0 MongoDB

## Build the Package
```bash
pipenv run build
```

