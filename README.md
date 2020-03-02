# guinea-bot
A guinea pig Twitter bot currently tweeting under the handle [@guinea_bot](https://twitter.com/guinea_bot)

It uses a very simple state machine implementation of a Markov chain (state changes are probabilistic rather than deterministic). 
A change of state is triggered every 15 minutes to emulate the exciting and busy life of a guinea pig. It randomly tweets what it 
is doing on each state change and may also post a random picture from its archive or search for other "guinea pig" accounts and 
randomly follow one. 

Tweets are selected from a JSON file, loaded on startup, that contains a variety of amusing messages for each state. For photos to
be tweeted the path to a folder of `.jpg` files must be set using the command line option on startup, a list of the photos available
to use is then loaded on startup.

Tweeting is limited to a 1 in 5 chance as it's very easy to generate hundreds of tweets a day. If nothing is tweeted
then there is a further 1 in 50 chance of tweeting a photo (if there are any) followed by a further 1 in 50 chance of trying to 
follow a new account.

The state machine prioritises sleeping and eating but the internal attributes can drive it from any state to any state,
see the code for the exact rules. Sleeping is used as the start state but there is no classical end state. The state
machine is currently coded to run for a fixed number of days, after which the guinea pig dies :cry:.

![Image of Guinea Pig States](https://raw.githubusercontent.com/RatJuggler/guinea-bot/master/gp-states.png)

## Installing
Checkout the source code from here:
```
$ git clone https://github.com/RatJuggler/guinea-bot.git
$ cd guinea-bot
```
Then install/update the bot as a Python package:
```
$ sudo pip3 install -U .
```
## Running
```
$ guineabot --help

Usage: guineabot [OPTIONS]

  Guinea Pig Twitter bot.

Options:
  --version                       Show the version and exit.
  -p, --photos-folder TEXT        Folder containing photos to Tweet.
  -l, --log-level [DEBUG|INFO|WARNING]
                                  Show additional logging information.
                                  [default: INFO]
  -q, --quiet                     Run without invoking the Twitter API.
                                  [default: False]
  --help                          Show this message and exit.
```
You can use the `-q` option to run without using the Twitter API but to make it fully functional you will need to set up a Twitter 
account and apply for access [here](https://developer.twitter.com/en/apply-for-access). You'll then need to make the following
tokens available to run it:
```
TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET
```
## Installing as a service
Copy the `guinea-bot.service` file to `/etc/systemd/system` to create a systemd unit service. 
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
