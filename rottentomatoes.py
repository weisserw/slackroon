from slackbot.bot import listen_to
 
import re
import urllib2
import json

from config import conf

@listen_to(r'^!r(t{1,3})\s+(.+)')
def do_movies(msg, num, search):
    search = search.strip()
    m = re.search(r'\s+(\d{4})$', search)
    year = None
    if m:
        year = search[-4:]
        search = search[:-4].strip()
    r = get_movies(len(num), search, year)
    if isinstance(r, list):
        msg.send_webapi('', json.dumps(r))
    else:
        msg.send(r)

@listen_to(r'^!dvd\s*$')
def do_dvd(msg):
    r = dvd()
    if isinstance(r, list):
        msg.send_webapi('', json.dumps(r))
    else:
        msg.send(r)

def get_movies(num, search, year):
    search = re.sub(r"[^a-zA-Z0-9,\-\.!'&\(\) ]", '', search)
    search = search.replace('&', '%26')
    search = search.replace(' ', '%20')
    search = search.replace('!', '%21')
    movies = json.loads(urllib2.urlopen("http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=%s&q=%s&page_limit=15" % (conf['rottentomatoes']['apikey'], search)).read())['movies']

    if year is not None:
        year = int(year)

    return parse_movies(num, movies, year, True)

def dvd():
    movies = json.loads(urllib2.urlopen("http://api.rottentomatoes.com/api/public/v1.0/lists/dvds/new_releases.json?apikey=%s&page_limit=5" % (conf['rottentomatoes']['apikey'],)).read())['movies']
    return parse_movies(5, movies, None)

def parse_movies(num, movies, year, detailed=False):
    if not len(movies):
        return 'No results.'

    ret = []
    for movie in movies:
        y = movie['year']
        if year is not None and year != y:
            continue
        title = movie['title']
        rating = movie['mpaa_rating']
        runtime = movie.get('runtime', '')
        critic = movie['ratings'].get('critics_score', -1)
        aud = movie['ratings'].get('audience_score', -1)
        synopsis = movie['synopsis']
        consensus = movie.get('critics_consensus', '')
        lnk = movie['links']['alternate']
        img = movie.get('posters', {}).get('original', None)
        thumb = movie.get('posters', {}).get('thumbnail', None)

        if critic < 0:
            critic = 'NR'
        else:
            critic = '%s%%' % critic
        if aud < 0:
            aud = 'NR'
        else:
            aud = '%s%%' % aud
        if consensus:
            consensus = ": %s" % consensus
        if runtime:
            runtime = '%sm' % runtime

        desc = ''
        if detailed:
            desc = '\n' + synopsis
            if len(desc) > 250:
                desc = desc[:247] + '...'
        ret.append({
            'fallback': "%s (%s) %s %s %s/%s%s%s" % (title, y, rating, runtime, critic, aud, consensus, desc),
            'text': "%s %s %s/%s%s%s" % (rating, runtime, critic, aud, consensus, desc),
            'title': "%s (%s)" % (title, y),
            'title_link': lnk,
        })
        if detailed:
            if img is not None:
                ret[-1]['image_url'] = img
            if thumb is not None:
                ret[-1]['thumb_url'] = thumb
        if len(ret) >= num:
            break
    if not len(ret):
        return 'No results.'
    return ret

