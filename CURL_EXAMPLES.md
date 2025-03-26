# Testing with ``curl``

- [Observability endpoints](#observability-endpoints)
     - [GET /api/config](#config)
     - [GET /api/health](#health)
- [Echo endpoints](#echo-endpoints)
     - [GET /api/echo](#get-agents)
     - [GET /api/echo/{agent}/{action}](#get-action)
     - [POST /api/echo/message/{id}](#process-a-message)
- [/api/bot endpoints](#apibot-endpoints)
     - [GET /api/bot](#get-a-list-all-active-of-bots)
     - [GET /api/bot/{id}](#get-a-single-bot)
     - [PATCH /api/bot/{id}](#update-a-single-bot)
     - [GET /api/bot/{id}/channels](#get-a-list-of-active-channels-the-bot-is-participating-in)
     - [POST /api/bot/{id}/channel/{channel}](#add-a-channel-to-the-active-channel-list)
     - [DELETE /api/bot/{id}/channel/{channel}](#remove-a-channel-from-the-active-channels-list)
- [/api/conversation endpoints](#apiconversation-endpoints)
     - [GET /api/conversation](#get-a-list-of-conversations-by-channel-name-regex)
     - [GET /api/conversation/{channel_id}](#get-a-single-conversation)
     - [POST /api/conversation/{channel_id}/message](#add-a-message-to-a-conversation)
     - [POST /api/conversation/{channel_id}/reset](#reset-a-conversation)
     - [POST /api/conversation/{channel_id}/load/{from_id}](#load-a-conversation)
     - [POST /api/conversation/{channel_id}/initialize](#initialize-a-conversation-from-a-csv-file)
     
## Observability endpoints

#### Config 
```sh
curl http://localhost:8580/api/config
```
#### Health 
```sh
curl http://localhost:8580/api/health
```

## Echo endpoints

#### Get Agents 
```sh
curl http://localhost:8580/api/echo
```
#### Get Action
```sh
curl http://localhost:8580/api/echo/bot/get_bot
```
#### Process a message
This will send a message through the same processing that happens on Discord and return the reply.
```sh
curl -X POST http://localhost:8580/api/echo/message/SOME_CHANNEL \
     -H "Content-Type: application/json" 
     -d '{"user": "mike", "text": "This is a new message"}'
```

## /api/bot endpoints 

#### Get a List all Active of Bots
```sh
curl http://localhost:8580/api/bot  
```
#### Get a single Bot
```sh
curl http://localhost:8580/api/bot/bbb000000000000000000001
```
#### Update a single Bot
```sh
curl -X PATCH http://localhost:8580/api/bot/bbb000000000000000000001 \
     -H "Content-Type: application/json" \
     -d '{"description":"A New Description"}'
```
#### Get a list of active channels the bot is participating in
```sh
curl http://localhost:8580/api/bot/bbb000000000000000000001/channels 
```
#### Add a channel to the active channel list
```sh
curl -X POST http://localhost:8580/api/bot/bbb000000000000000000001/channel/DISCORD_CHANNEL_NAME
```
#### Remove a channel from the active channels list
```sh
curl -X DELETE http://localhost:8580/api/bot/bbb000000000000000000001/channel/DISCORD_CHANNEL_NAME
```

## /api/chain endpoints 

#### Get a list of all Exercise Chains
```sh
curl http://localhost:8580/api/chain
```
#### Get a single Exercise Chain
```sh
curl http://localhost:8580/api/chain/a00000000000000000000001
```

## /api/conversation endpoints

#### Get a list of conversations by channel name regex
```sh
curl http://localhost:8580/api/conversation
```
#### Get a single Conversation
```sh
curl http://localhost:8580/api/conversation/c00000000000000000000001
```
#### Add a message to a conversation
```sh
curl -X POST http://localhost:8580/api/conversation/DISCORD_01/message \
     -H "Content-Type: application/json" \
     -d '{"role": "user", "content": "From:Me To:group This is a new message"}'
```
#### Reset a conversation
This will update the version, and set the status to complete, leaving no active conversation for this channel. A new active:latest conversation will be created when it is needed. 
```sh
curl -X POST http://localhost:8580/api/conversation/DISCORD_01/reset \
     -H "Content-Type: application/json" 
```
#### Load a conversation
This will copy all the messages from a named conversation (i.e. Echo) into the SOME_CHANNEL conversation
```sh
curl -X POST http://localhost:8580/api/conversation/SOME_CHANNEL/load/Echo \
     -H "Content-Type: application/json" 
```

#### Initialize a conversation from a CSV file.
This will reset the conversation an then load all the rows from a csv file into the new conversation.
```sh
curl -X POST "http://localhost:8580/api/conversation/SOME_CHANNEL/initialize" \
     -H "Content-Type: text/csv" \
     --data-binary "@./fran_model/prompts/echo.csv"
```

## /api/exercise endpoints

#### Get a list of all active exercises
```sh
curl http://localhost:8580/api/exercise
```
#### Get a single exercise
```sh
curl http://localhost:8580/api/exercise/b00000000000000000000001
```

## /api/workshop endpoints

#### Get a list of all active workshops by workshop name regex
```sh
curl "http://localhost:8580/api/workshop"
```
#### Get a list of workshops by workshop name regex
```sh
curl "http://localhost:8580/api/workshop?query=^p"
```
#### Get a specific workshop
```sh
curl "http://localhost:8580/api/workshop/000000000000000000000001"
```
#### Add a new Workshop
```sh
curl -X POST http://localhost:8580/api/workshop/new/a00000000000000000000001 \
     -H "Content-Type: application/json" \
     -d '{"name":"Super Duper Workshop"}'
```
#### Update a workshop
```sh
curl -X PATCH http://localhost:8580/api/workshop/000000000000000000000001 \
     -H "Content-Type: application/json" \
     -d '{"name":"Updated Workshop Name"}'
```
#### Start a workshop - Status to active
```sh
curl -X POST http://localhost:8580/api/workshop/000000000000000000000001/start
```
#### Advance to the next exercise in the workshop
```sh
curl -X POST http://localhost:8580/api/workshop/000000000000000000000001/next
```
#### Add an observation to the current exercise
```sh
curl -X POST http://localhost:8580/api/workshop/000000000000000000000001/observation \
     -H "Content-Type: application/json" \
     -d '{"name":"Observation1"}'
```