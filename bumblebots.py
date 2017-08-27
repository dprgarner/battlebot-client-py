import json
import random

from client import Client


CHAR_TO_INT = {
    '.': 0,
    '#': 1,
    '£': 2,
    '+': 5,
    'x': 6,
};
INT_TO_CHAR = {v: k for k, v in CHAR_TO_INT.items()}


MOVES = ['UL', 'UR', 'R', 'DR', 'DL', 'L']


class BumblebotsClient(Client):
    GAME_TYPE = 'BUMBLEBOTS'

    def render_board(self, board, drones=None):
        """
        Render the board as a string, with (optionally) drones on top.
        Friendly drones are rendered as "@", enemy drones with "&".
        """
        drone_positions = {}
        for name, drones_by_name in (drones or {}).items():
            for drone in drones_by_name.values():
                drone_positions[tuple(drone['position'])] = (
                    '@' if self.name == name else '&'
                )

        string_rows = []
        for i, row in enumerate(board):
            str_ = ''
            for j, c in enumerate(row):
                if c or str_:
                    str_ += drone_positions.get((i, j), INT_TO_CHAR[c]) + ' '
            string_rows.append(str_.strip())

        max_width = len(board)
        for i in range(max_width):
            add_padding = int(abs((max_width - 1) / 2 - i))
            string_rows[i] = ' ' * add_padding + string_rows[i]
        return '\n{}\n'.format('\n'.join(string_rows))


    def play_game(self):
        """
        Brownian motion.
        """
        while True:
            update = self.recv()
            if not update:
                return
            print('turn:', update['turnNumber'])
            print(self.render_board(update['board'], update['drones']))

            orders = {
                drone: random.choice(MOVES)
                for drone in update['drones'][self.name]
            }
            self.send({'orders': orders})


if __name__ == '__main__':
    BumblebotsClient()
