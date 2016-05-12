from config import conf

API_TOKEN = conf['token']

DEFAULT_REPLY = 'Sobweh...'

ERRORS_TO = conf['erruser']

PLUGINS = [
	'twitter',
	'weather',
	'weight',
	'wikipedia',
]
