from flask import Flask

from flask_basicauth import BasicAuth

server = Flask(__name__)


with open('.pass') as f:
    VALID_USERNAME_PASSWORD_PAIRS = [x.strip().split(':') for x in f.readlines()]

username = VALID_USERNAME_PASSWORD_PAIRS[0][0]
password = VALID_USERNAME_PASSWORD_PAIRS[0][1]

server.config['BASIC_AUTH_USERNAME'] = username
server.config['BASIC_AUTH_PASSWORD'] = password
server.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(server)
