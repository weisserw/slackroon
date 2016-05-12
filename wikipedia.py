from slackbot.bot import listen_to

import re
import json
import urllib2

from config import conf

@listen_to(r'^!wiki\s+(.*)')
def wikipedia(message, title):
    # replace spaces with underscores and capitalize first letter of each word in title per wikipedia being an ass
    title = str.replace(title, ' ', '_').title()
    e = getExtract(title)
    if e is None:
        results = search(title)
        if results is None or len(results) == 0:
            message.send('No articles found.')
        else:
            title = results[0]
            e = getExtract(results[0])
            if e is None:
                message.send_webapi('', json.dumps([{
                    'fallback': result,
                    'text': '<https://en.wikipedia.org/wiki/%s|%s>' % (result.replace(' ', '_'), result)
                } for result in results]))
    if e is not None:
        message.send_webapi('', json.dumps([{
            'fallback': e,
            'text': '<https://en.wikipedia.org/wiki/%s|%s>' % (title.replace(' ', '_'), e)
        }]))

def getExtract(title):
    url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=' + title
    
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    f.close()
    
    pages = parsed_json['query']['pages']
    
    # the key under pages is dynamic based upon the article id
    if pages.keys()[0] == '-1':
        return None
    
    extract = pages[pages.keys()[0]]['extract']
    
    # empty extract or if there are multiple reults the extract will just contain the term plus "may refer to""
    if (not extract) or (extract.find('may refer to:') != -1):
        return None
    
    if len(extract) == 200:
        return extract
    
    return extract[:200] + '...'
    
def search(title):
    url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&utf8=&srsearch=' + title
    
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    f.close()
    
    if parsed_json['query']['searchinfo']['totalhits'] == 0:
        return None
    
    results = parsed_json['query']['search']
    titles = []
    
    for result in results:
        titles.append(result['title'])
    
    # 3 top results seems like enough
    return titles[:3]
