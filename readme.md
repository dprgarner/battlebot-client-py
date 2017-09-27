# Battlebot Client

This is a Python client for AI battles! This is a boilerplate repository for quickly getting a bot set up that can connect and authenticate with the server. How the bot implements and plays the game is up to you.

The server is currently being hosted on Heroku: https://blunderdome-server.herokuapp.com/

Server code here: https://github.com/dprgarner/battlebot-server

## Registering

Before playing a game, each bot needs to register with the server. This consists of making a POST request to the GraphQL endpoint `/graphql`, consisting of the game type, the name of the bot, and your name. The server will return a response containing the bot data and the password, which is used to authenticate the bot when connecting via websocket. This registration can be done via the online GraphiQL interface at `/graphql`.

The provided helper file `register.py` will make this request and save the JSON file to `auth.json`. To save the authentication data to a different file, add the `--auth` parameter, e.g. `--auth=auth2.json`.

```bash
> $ python register.py --hostname=blunderdome-server.herokuapp.com --gametype=NOUGHTS_AND_CROSSES --owner=David --name=MyAwesomeBot
Bot MyAwesomeBot registered successfully
> $ cat auth.json
{
  "hostname": "blunderdome-server.herokuapp.com",
  "password": "8ad86f2934f347abf60ee7c192c96fbc8383de273c4c092de7ae97151b84d934",
  "name": "MyAwesomeBot"
}
```

## Connecting

When a websocket connection is made, after the initial WebSocket handshake, the client should send a JSON object containing the game type `gameType`, the name of the bot `name`, and the bot's password `password`. The server will then return the JSON `{ "authentication": "ok" }` if the login is successful, or disconnect if not. If the authentication is successful, the server will pair the bot off with any other connected bot to a start a game, or will maintain the connection if no other connected bots are available.

The provided helper file `client.py` will handle the connection to the server, using the saved `auth.json` file, and wait for a game to start.

```bash
> $ python client.py
Bot connected - waiting to start game...
Traceback (most recent call last):
  File "client.py", line 79, in <module>
    Client()
  File "client.py", line 15, in __init__
    self.play_game()
  File "client.py", line 75, in play_game
    raise NotImplementedError('Write your bot\'s logic here.')
NotImplementedError: Write your bot's logic here.
```

The provided client.py file should be modified or extended with your custom logic for running the game.  All communication between the client and server is via JSON, so the client provides the two helper methods `recv`, which pauses until the server sends some data and then decodes it to an object, and `send`, which encodes a JSON-serialisable object and sends the data to the server. If the server closes the connection, the method `recv` will return None.

## Contests

To play in a contest, add the name of the contest as an argument, e.g.
```bash
> $ python client.py --contest=round-robin
```
The client will add an extra key to the login hash and will repeatedly attempt to reconnect after each game is played. The server will match up bots which are playing in the contest with other bots in the contest, provided that they have played each other less than five times in the contest. The API endpoint `/games/<game_name>/contest/<contest_name>` gives a summary of the games played in the contest and the rankings of the bots. A bot scores three points for a win, one point for a draw, and no points for a loss. Ties are broken on most wins, then fewest losses.

## Noughts and Crosses

As soon as a game starts, the server will send an update of the following form to the client bot:
```javascript
{
  "state": {
    "bots": [
      "IdiotBot2",
      "IdiotBot"
    ],
    "complete": false,
    "board": [
      [
        "",
        "",
        ""
      ],
      [
        "",
        "",
        ""
      ],
      [
        "",
        "",
        ""
      ]
    ],
    "waitingFor": ["IdiotBot2"],
    "marks": {
      "X": "IdiotBot2",
      "O": "IdiotBot"
    }
  }
}
```

The client sends turns to the server, and the server validates the turn and responds with the new state and the played turn.  A turn dispatched from the client to the server should look like this:

```javascript
{
  "mark": "X",
  "space": [2, 2]
}
```

A space is specified as a two-entry array, with each entry an integer from 0 to 2, specifying the row and column to place the mark in respectively.  The mark should be "O" or "X", depending on whether the client is playing "X"es or "O"s.

The following is an example of a server response, at the end of the game:

```javascript
{
  "turn": {
    "name": "IdiotBot2",
    "valid": true,
    "space": [1, 2],
    "time": 1498036964996,
    "mark": "X"
  },
  "state": {
    "complete": true,
    "bots": [
      "IdiotBot2",
      "IdiotBot"
    ],
    "reason": "complete",
    "board": [
      [
        "O",
        "O",
        "X"
      ],
      [
        "X",
        "O",
        "X"
      ],
      [
        "O",
        "X",
        "X"
      ]
    ],
    "marks": {
      "X": "IdiotBot2",
      "O": "IdiotBot"
    },
    "waitingFor": ["IdiotBot"],
    "victor": "IdiotBot2"
  }
}
```

If a bot disconnects the websocket during the course of the game, then the bot is disqualified. If the bot makes three invalid moves, or takes longer than five seconds to play a move, then the bot is disqualified.

If you want to test your bot out, I'd suggest registering a second bot and having them play each other. I've also written a bot which randomly plays valid noughts and crosses turns, but doesn't really have any strategy - I can spin this up to repeatedly connect to the server when someone wants to try their own bot out.

Happy bot-writing!

# Licence
ISC
