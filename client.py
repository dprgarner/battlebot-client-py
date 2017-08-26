from os import path
import json
import hashlib
import argparse

from websocket import create_connection


class Client(object):
    GAME_TYPE = 'NOUGHTS_AND_CROSSES'

    def __init__(self):
        self.set_args()
        self.set_auth_data()

        if self.contest:
            while True:
                self.connect()
        else:
            self.connect()

    def connect(self):
        try:
            self.ws = create_connection('wss://{}'.format(self.hostname))
            self.authenticate()
            print('Bot connected - waiting to start game...')
            self.play_game()
        finally:
            if hasattr(self, 'ws') and self.ws.connected:
                self.ws.close()

    def send(self, msg):
        """
        All messages to the server must be JSON-serialisable.
        """
        self.ws.send(json.dumps(msg))

    def recv(self):
        """
        All messages from the server are valid JSON.
        """
        msg = self.ws.recv()
        return (
            json.loads(msg)
            if msg
            else msg
        )

    def set_args(self):
        parser = argparse.ArgumentParser(
            description='Python Battlebot Client'
        )
        parser.add_argument(
            '--auth',
            type=str,
            default='auth.json',
            help='Use a bot credentials JSON file. (Default: auth.json)',
        )
        parser.add_argument(
            '--contest',
            type=str,
            default='',
            help='Take part in a contest.',
        )
        args = parser.parse_args()
        for k, v in args._get_kwargs():
            setattr(self, k, v)

    def set_auth_data(self):
        auth_file = path.join(
            path.dirname(path.realpath(__file__)),
            self.auth,
        )
        with open(auth_file) as f:
            data = json.loads(f.read())
        for k, v in data.items():
            setattr(self, k, v)

    def authenticate(self):
        # On connect, send a "login" message to the server.
        login_message = {
            'name': self.name,
            'password': self.password,
            'gameType': self.GAME_TYPE,
        }
        if self.contest:
            login_message['contest'] = self.contest
        self.send(login_message)

        auth_response = self.recv()
        if (
            not auth_response or
            not self.ws.connected or
            auth_response['authentication'] != 'OK'
        ):
            raise Exception('Failed to connect and authenticate.')

    def play_game(self):
        """
        Override this method to implement your bot!
        """
        raise NotImplementedError(
            "Write your bot's logic here. (Or even better: extend this class.)"
        )


if __name__ == '__main__':
    Client()
