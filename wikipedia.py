from slackbot.bot import listen_to

import re
import json
import urllib2

from config import conf

@listen_to(r'!wiki\s+(.*)')
def wikipedia(message, title):
    # replace spaces with underscores and capitalize first letter of each word in title per wikipedia being an ass
    title = str.replace(title, ' ', '_').title()
    e = getExtract(title)
    if e == None:
        results = search(title)
        if results == None:
            message.send('No article found.')
        else:
            for result in results:
                message.send_webapi('', json.dumps([{
                    'fallback': result,
                    'title': result,
                    'title_link': 'https://en.wikipedia.org/wiki/' + result.replace(' ', '_')
        }])) 
    else:
        message.send_webapi('', json.dumps([{
            'fallback': e,
            'title': e,
            'title_link': 'https://en.wikipedia.org/wiki/' + title.replace(' ', '_')
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
    
    # if there are multiple reults the extract will just contain the term plus "may refer to""
    if extract.find('may refer to:') != -1:
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
    
    # 5 top results seems like enough
    return titles[:5]