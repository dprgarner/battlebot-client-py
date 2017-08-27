from os import path
import json

import argparse
import requests

parser = argparse.ArgumentParser(
    description='Register the bot to the server and locally save the login credentials.'
)
parser.add_argument(
    '--name',
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
    '--gametype',
    type=str,
    required=True,
    help='The name of the game, e.g. NOUGHTS_AND_CROSSES.'
)
parser.add_argument(
    '--owner',
    type=str,
    default='Anonymous',
    help='The owner of the bot. (Default: Anonymous)'
)
parser.add_argument(
    '--auth',
    type=str,
    default='auth.json',
    help='Save the bot credentials JSON to a different file. (Default: auth.json)'
)
parser.add_argument(
    '--nossl',
    dest='no_ssl',
    action='store_const',
    const=True,
    default=False,
    help='Connect to the server without SSL.'
)

args = parser.parse_args()

hostname = (
    args.hostname[:-1]
    if args.hostname.endswith('/')
    else args.hostname
)
protocol = 'http' if args.no_ssl else 'https'
url = '{}://{}/graphql'.format(protocol, hostname)

query = """
mutation($gameType: GameType!, $name: ID!, $owner: String!) {
  registerBot(gameType: $gameType, name: $name, owner: $owner) {
    password
    bot {
      name
      owner
      gameType
      dateRegistered
    }
  }
}
"""

variables = {
    'name': args.name,
    'owner': args.owner,
    'gameType': args.gametype,
}

response = requests.post(url, json={
    'query': query,
    'variables': variables,
})

if not response.ok:
    raise Exception(response.text)
data = response.json()
if data.get('errors'):
    raise Exception(data['errors'])

print('Bot {} registered successfully'.format(args.name))

auth_data = {
    'hostname': hostname,
    'name': args.name,
    'password': data['data']['registerBot']['password'],
}
json_file = path.join(path.dirname(path.realpath(__file__)), args.auth)

with open(json_file, 'w') as f:
    f.write(json.dumps(auth_data, indent=2))
print('Bot data saved to {}'.format(json_file))
