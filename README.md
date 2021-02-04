# guinea-bot

![Test & QA](https://github.com/RatJuggler/guinea-bot/workflows/Test%20&%20QA/badge.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/RatJuggler/guinea-bot)

A guinea pig Twitter bot currently tweeting under the handle [@guinea_bot](https://twitter.com/guinea_bot)

It uses a very simple state machine implementation of a Markov chain (some state changes are probabilistic rather than 
deterministic). The state machine runs with a change of state triggered being every 15 minutes (by default). The guinea pig has a 
lifespan, and some simple internal attributes which affect its behaviour to emulate its exciting and busy life. It will randomly 
tweet what it is doing on each state change and may also post a random picture from its archive if configured to do so. 

Tweets are selected from a JSON file, loaded on start-up, that contains a variety of amusing messages for each state. For photos to
be tweeted the path to a folder of `.jpg` files must be set using the command line option, a list of the photos available to use is 
then loaded on start-up. Tweeting is limited to a 1 in 8 chance as it's very easy to generate hundreds of tweets a day. If the 
state doesn't change then there is a 1 in 80 chance of tweeting a photo (if there are any).

The bot has the functionality to automatically search for other guinea pigs related accounts and randomly follow them. This was 
triggered with a 1 in 80 chance if nothing was tweeted, but having bots automatically follow other accounts on Twitter is a bit of 
minefield as you never know what you are going to get so this functionality has been disabled. When enabled the bot searched for 
accounts using the "#guineapig" tag and then decide if it wanted to follow them after checking for a number of "red flag" keywords 
in the accounts' bio/description. It also attempts to curate the existing friends list by removing friends who no longer pass the 
"friendship test", unless they are following back, in which case they are muted. 

The state changes that drive the guinea pig prioritise sleeping and eating, but the internal attributes can drive it from any state 
to any other state (see the code for the exact rules). Sleeping is used as the start state, and the end state can be reached at any 
time as the guinea pig ages, reaches its lifespan duration and dies :cry:. But, the internal state, age/attributes, are persisted 
to a file on each state change so that the same guinea pig can continue to run after a crash or power outage. The file is stored in
the current users home directory, there is no option to change this yet.

![Image of Guinea Pig States](https://raw.githubusercontent.com/RatJuggler/guinea-bot/master/gp-states.png)

## Installing

Checkout the source code from here:

    $ git clone https://github.com/RatJuggler/guinea-bot.git
    $ cd guinea-bot

Then install/update the bot as a Python package:

    $ pip3 install -U .

## Running
```
$ guineabot --help

Usage: guineabot [OPTIONS]

  Guinea Pig Twitter bot.

Options:
  --version                       Show the version and exit.
  -n, --name TEXT                 The name of the guinea pig.  [default:
                                  Holly]
  -h, --house DIRECTORY           Piggy house where the guinea pig is kept.
                                  [default: (user home directory)]
  -p, --photos DIRECTORY          Optional path to photos which can be
                                  Tweeted.
  -d, --duration INTEGER RANGE    How many days the bot should run for (guinea
                                  pig lifespan), random if not set.
  -i, --interval INTEGER RANGE    The interval between changes in state
                                  (guinea pig activity), in minutes.
                                  [default: 15]
  -a, --accelerated               Ignore the pauses between state changes,
                                  forces quiet mode to prevent Twitter API
                                  rate limit triggering.  [default: False]
  -l, --log-level [DEBUG|INFO|WARNING]
                                  Show additional logging information.
                                  [default: INFO]
  -q, --quiet                     Run without invoking the Twitter API.
                                  [default: False]
  -t, --test                      Test the Twitter access tokens and exit.
                                  [default: False]
  --help                          Show this message and exit.
```
You can use the `-q` option to run without using the Twitter API but to make it fully functional you will need to set up a Twitter 
account and apply for access [here](https://developer.twitter.com/en/apply-for-access). You'll then need to make the following
tokens available to run it:

    TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET
    TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_TOKEN_SECRET

Test that your tokens are working by using:

    $ guineabot --test

## Installing as a service under systemd

First edit the `guinea-bot.service` file and add any command line options you need, making sure to keep them within the command 
quotes. It's also a good idea to set a user as the service does not need to run as root, but make sure the home directory is 
accessible if you are using the default state save location. Once complete copy the file to `/etc/systemd/system` and enter the 
following to create a systemd unit service. 

    $ sudo cp guinea-bot.service /etc/systemd/system

A configuration file also needs to be created to hold the Twitter access keys.

    $ sudo systemctl edit guinea-bot

Add an entry to the generated file like so:

    [Service]
    Environment="TWITTER_CONSUMER_KEY=<your consumer key here>"
    Environment="TWITTER_CONSUMER_SECRET=<your consumer secret here>"
    Environment="TWITTER_ACCESS_TOKEN=<your access token here>"
    Environment="TWITTER_ACCESS_TOKEN_SECRET=<your access token secret here>"

Reload the service files after changes or when new:

    $ sudo systemctl daemon-reload

Enable the service:

    $ sudo systemctl enable guinea-bot.service

Start the service:

    $ sudo systemctl start guinea-bot.service

Check the status of the service:

    $ sudo systemctl status guinea-bot.service

Stop the service:

    $ sudo systemctl stop guinea-bot.service

Tail service's log:

    $ sudo journalctl -f -u guinea-bot.service

## Docker

Docker build and compose files are available which create a standalone image for the guinea bot to live in.

Create the image with: `docker build -f docker/Dockerfile -t guinea-bot:local .`

We need to be careful that any Twitter access tokens aren't included in the image in case it is pushed to a public repository (and
it's also just best practice). There are a number of ways to inject the tokens into the image but probably the easiest is to create 
an `env.list` file from the supplied template, set the tokens in it and then run the image with the `--env-file` option.

    docker run guinea-bot:local -d --env-file ./docker/env.list

Or just use the compose file to do everything:

    docker-compose up -d
