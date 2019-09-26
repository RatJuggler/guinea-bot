# guinea-bot
A guinea pig Twitter bot currently tweeting under the handle [@guinea_bot](https://twitter.com/guinea_bot)

It uses a very simple state machine, which changes state every 15 minutes, to emulate the exciting and busy life of a
guinea pig. It randomly tweets what it is doing on each state change and may also post a random picture from its archive
or search for other "guinea pig" accounts and randomly follow one. 

Tweets are selected from a JSON file, loaded on startup, that contains a variety of amusing messages for each state. A
list of the photos to use is also loaded on startup, see the code to change the folder photos are read from.

Tweeting is limited to a 2 in 10 chance as it's very easy to generate hundreds of tweets a day. If nothing is tweeted
then there is a further 1 in 50 chance of tweeting a photo followed by a further 1 in 50 chance of trying to follow a
new account.

The state machine prioritises sleeping and eating but the internal attributes can drive it from any state to any state,
see the code for the exact rules. Sleeping is used as the start state but there is no classical end state. The state
machine is currently coded to run for a fixed number of days, after which the guinea pig dies :cry:.

![Image of Guinea Pig States](https://raw.githubusercontent.com/RatJuggler/guinea-bot/master/gp-states.png)

# Install as a service

Checkout the source code from here:
```
$ git clone https://github.com/RatJuggler/guinea-bot.git
$ cd guinea-bot
```
Then install/update the bot as a Python package:
```
$ sudo pip3 install -U .
```
The `guinea-bot.service` file can now be copied to `/etc/systemd/system` to create a systemd unit service. 
```
$ cp guinea-bot.service /etc/systemd/system
```
A configuration file also needs to be created to hold the Twitter access keys.
```
$ sudo systemctl edit guinea-bot
```
Add an entry to the generated file like so:
```
[Service]
Environment="TWITTER_CONSUMER_KEY=<your consumer key here>"
Environment="TWITTER_CONSUMER_SECRET=<your consumer secret here>"
Environment="TWITTER_ACCESS_TOKEN=<your access token here>"
Environment="TWITTER_ACCESS_TOKEN_SECRET=<your access token secret here>"
```
Reload the service files after changes or when new:
```
$ sudo systemctl daemon-reload
```
Enable the service:
```
$ sudo systemctl enable guinea-bot.service
```
Start the service:
```
$ sudo systemctl start guinea-bot.service
```
Check the status of the service:
```
$ sudo systemctl status guinea-bot.service
```
Stop the service:
```
$ sudo systemctl stop guinea-bot.service
```
Tail service's log:
```
$ sudo journalctl -f -u guinea-bot.service
```
