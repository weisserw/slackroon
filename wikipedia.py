from slackbot.bot import listen_to

import re
import json
import urllib2

from config import conf

@listen_to(r'!wiki\s+(.*)')
def wikipedia(message, title):
    e = getExtract(title)
    if e == None:
        message.send('No article found.')
    else:
        message.send_webapi('', json.dumps([{
            'fallback': e,
            'title': e,
            'title_link': 'https://en.wikipedia.org/wiki/' + title
        }]))

def getExtract(title):
    url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=' + title
    
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    f.close()
    
    pages = parsed_json['query']['pages']
    
    if pages.keys()[0] == '-1':
        return None
    
    extract = pages[pages.keys()[0]]['extract']
    
    if len(extract) == 200:
        return extract
    
    return extract[:200] + '...'