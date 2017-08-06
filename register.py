from os import path
import json

import argparse
import requests

parser = argparse.ArgumentParser(
    description='Register the bot to the server and locally save the login credentials.'
)
parser.add_argument(
    '--bot',
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
    '--auth',
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
url = 'http://{}/graphql'.format(hostname)


query = """
mutation($name: ID!, $gameType: ID!, $owner: String!) {
  registerBot(name: $name, gameType: $gameType, owner: $owner) {
    password
    bot {
      id
      owner
      gameType {
        id
      }
      dateRegistered
    }
  }
}
"""

variables = {
    'gameType': args.game,
    'name': args.bot,
    'owner': args.owner,
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

print('Bot {} registered successfully'.format(args.bot))

auth_data = {
    'hostname': hostname,
    'game': args.game,
    'bot': args.bot,
    'password': data['data']['registerBot']['password'],
}
json_file = path.join(path.dirname(path.realpath(__file__)), args.auth)

with open(json_file, 'w') as f:
    f.write(json.dumps(auth_data, indent=2))
print('Bot data saved to {}'.format(json_file))
