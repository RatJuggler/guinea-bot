# guinea-bot
A guinea pig Twitter bot currently tweeting under the handle [@guinea_bot](https://twitter.com/guinea_bot)

Uses a very simple state machine, which changes state every 15 minutes, to emulate the exciting and busy life of a
guinea pig and tweets what it is doing.

Tweets are selected from a JSON file, loaded on startup, that contains a variety of amusing messages for each state.
