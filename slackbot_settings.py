from config import conf

API_TOKEN = conf['token']

DEFAULT_REPLY = 'Sobweh...'

ERRORS_TO = conf['erruser']

PLUGINS = [
    'roontwitter',
    'rottentomatoes',
    'weather',
    'weight',
    'wikipedia',
]
