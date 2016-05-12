from slackbot.bot import listen_to

import re
import json
import urllib
import urllib2

from TwitterSearch import TwitterSearch, TwitterSearchOrder, TwitterUserOrder, TwitterSearchException
import twitter

from config import conf

ts = TwitterSearch(
    consumer_key = conf['twitter']['consumer_key'],
    consumer_secret = conf['twitter']['consumer_secret'],
    access_token = conf['twitter']['access_token'],
    access_token_secret = conf['twitter']['access_token_secret']
)
api = twitter.Api(
    consumer_key = conf['twitter']['consumer_key'],
    consumer_secret = conf['twitter']['consumer_secret'],
    access_token_key = conf['twitter']['access_token'],
    access_token_secret = conf['twitter']['access_token_secret']
)

@listen_to(r'^!tr(\s+.*)?')
def do_trends(msg, loc):
    if loc:
        loc = loc.strip()
    if not loc:
        loc = 'usa'
    url = "http://where.yahooapis.com/v1/places.q('" + loc + "')?appid=" + conf['twitter']['yahoo_appid'];
    content = urllib2.urlopen(url).read()

    woeid = 1
    m = re.search(r'<woeid>([^<]+)', content)
    if m:
        woeid = int(m.group(1).strip())
    trends = api.GetTrendsWoeid(woeid)
    names = []
    for t in trends:
        if ' ' in t.name:
            names.append('"%s"' % t.name)
        else:
            names.append(t.name)
        if len(names) > 9:
            break
    msg.send_webapi('', json.dumps([{
        'fallback': " ".join(names),
        'text': " ".join("<https://twitter.com/search?q=%s|%s>" % (n, n) for n in names)
    }]))

@listen_to(r'^!t(u{1,3})\s+(.*)')
def do_user(msg, num, search):
    try:
        tuo = TwitterUserOrder(search)

        i = 0
        for tweet in ts.search_tweets_iterable(tuo):
            msg.send('http://twitter.com/%s/status/%s' % (tweet['user']['screen_name'], tweet['id']))
            i += 1
            if i >= len(num):
                break
    except TwitterSearchException, e:
        if e.code == 401:
            msg.send('Timeline is private')
        else:
            raise e

@listen_to(r'^!t(s{1,3})\s+(.*)')
def do_search(msg, num, search):
    tso = TwitterSearchOrder()
    search = search.replace('&amp;', '&')
    tso.set_search_url('q=%s' % urllib.quote(search))
    tso.set_language('en')
    tso.set_include_entities(False)
    tso.set_count(len(num))
    tso.add_keyword('-RT')
    tso.set_result_type('recent')

    i = 0
    for tweet in ts.search_tweets_iterable(tso):
        msg.send('http://twitter.com/%s/status/%s' % (tweet['user']['screen_name'], tweet['id']))
        i += 1
        if i >= len(num):
            break
