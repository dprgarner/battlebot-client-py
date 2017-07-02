from os import path
import json

import argparse
import requests

parser = argparse.ArgumentParser(
    description='Register the bot to the server and locally save the login credentials.'
)
parser.add_argument(
    'bot_id',
    type=str,
    help='The name of the bot.'
)
parser.add_argument(
    '--hostname',
    type=str,
    required=True,
    help='The hostname of the bot server. (e.g. blunderdome-server.herokuapp.com)'
)
parser.add_argument(
    '--game',
    type=str,
    required=True,
    help='The name of the game.'
)
parser.add_argument(
    '--owner',
    type=str,
    default='Anonymous',
    help='The owner of the bot. (Default: Anonymous)'
)
parser.add_argument(
    '--authfile',
    type=str,
    default='auth.json',
    help='Save the bot credentials JSON to a different file. (Default: auth.json)'
)

args = parser.parse_args()

hostname = (
    args.hostname[:-1]
    if args.hostname.endswith('/')
    else args.hostname
)
url = 'https://{}/bots/{}'.format(hostname, args.game)

response = requests.post(url, json={
    'bot_id': args.bot_id,
    'owner': args.owner,
})
if not response.ok:
    raise Exception(response.text)
print('Bot {} registered successfully'.format(args.bot_id))

data = response.json()
data['hostname'] = hostname
json_file = path.join(path.dirname(path.realpath(__file__)), args.authfile)

with open(json_file, 'w') as f:
    f.write(json.dumps(data, indent=2))
print('Bot data saved to {}'.format(json_file))
