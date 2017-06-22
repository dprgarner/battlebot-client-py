import json
from client import Client


class NumberwangClient(Client):
    def play_game(self):
        """
        A simple, memoryless, implementation of a game-playing bot.
        """
        while True:
            update = self.recv()
            if not update:
                return

            if update['state']['complete']:
                print('{} has won the game.'.format(update['state']['victor']))
                return

            print(json.dumps(update, indent=2))
            if update['state']['nextPlayer'] == self.bot_id:
                turn = self.play_turn(update['state'])
                self.send(turn)

    def play_turn(self, state):
        return {'n': 2}


if __name__ == '__main__':
    NumberwangClient()