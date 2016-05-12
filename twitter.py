from slackbot.bot import listen_to

import re
import urllib

from TwitterSearch import TwitterSearch, TwitterSearchOrder, TwitterUserOrder

from config import conf

ts = TwitterSearch(
	consumer_key = conf['twitter']['consumer_key'],
	consumer_secret = conf['twitter']['consumer_secret'],
	access_token = conf['twitter']['access_token'],
	access_token_secret = conf['twitter']['access_token_secret']
)

@listen_to(r'!t(u{1,3})\s+(.*)')
def do_user(msg, num, search):
	tuo = TwitterUserOrder(search)

	i = 0
	for tweet in ts.search_tweets_iterable(tuo):
		msg.send('http://twitter.com/%s/status/%s' % (tweet['user']['screen_name'], tweet['id']))
		i += 1
		if i >= len(num):
			break
		
@listen_to(r'!t(s{1,3})\s+(.*)')
def do_search(msg, num, search):
	tso = TwitterSearchOrder()
	search = search.replace('&amp;', '&')
	tso.set_search_url('q=%s' % urllib.quote(search))
	tso.set_language('en')
	tso.set_include_entities(False)
	tso.set_count(len(num))
	tso.add_keyword('-RT')
	tso.set_result_type('recent')

	#print tso.create_search_url()

	i = 0
	for tweet in ts.search_tweets_iterable(tso):
		msg.send('http://twitter.com/%s/status/%s' % (tweet['user']['screen_name'], tweet['id']))
		i += 1
		if i >= len(num):
			break
