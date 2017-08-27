import json
import random

from client import Client


class NoughtsAndCrossesClient(Client):
    GAME_TYPE = 'NOUGHTS_AND_CROSSES'

    def play_game(self):
        """
        A simple, memoryless, implementation of a game-playing bot. Should work
        for most two-player abstract strategy games.
        """
        while True:
            update = self.recv()
            if not update:
                return

            print(json.dumps(update, indent=2))

            if update['state'].get('result'):
                victor = update['state']['result'].get('victor')
                print(
                    '{} has won the game.'.format(victor)
                    if victor
                    else 'The game was a draw.'
                )
                return

            if self.name in update['state']['waitingFor']:
                turn = self.play_turn(update['state'])
                self.send(turn)

    def play_turn(self, state):
        """
        Just keep choosing random spaces until an empty one is found.
        """
        board = state['board']
        i = 0
        while i < 10000:
            space = (random.randrange(3), random.randrange(3))
            if not board[space[0]][space[1]]:
                break
            i += 1
        mark = (
            'X'
            if state['marks']['X'] == self.name
            else 'O'
        )
        return {'space': [space[0], space[1]], 'mark': mark}


if __name__ == '__main__':
    NoughtsAndCrossesClient()
