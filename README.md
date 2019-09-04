# guinea-bot
A guinea pig Twitter bot currently tweeting under the handle [@guinea_bot](https://twitter.com/guinea_bot)

Uses a very simple state machine, which changes state every 15 minutes, to emulate the exciting and busy life of a
guinea pig. Randomly tweets what it is doing on each state change. Also searches for other "guinea pig" accounts and 
will randomly follow one. 

Tweets are selected from a JSON file, loaded on startup, that contains a variety of amusing messages for each state.
Tweeting is limited to a 1 in 10 chance as it's very easy to generate hundreds of tweets a day, similarly following is
limited to a 1 in 200 chance.
