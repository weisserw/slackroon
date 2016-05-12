from slackbot.bot import listen_to

import re
import json
import urllib2

from config import conf

@listen_to(r'!wi\s+(.*)')
def do_weight(msg, user):
	s = None
	user = user.strip()
	if user not in conf['weight']['users']:
		msg.send('No such user')
		return
	udata = conf['weight']['users'][user]
	if udata['type'] == 'fitbit':
		req = urllib2.Request('https://www.fitbit.com/user/%s/weight' % (udata['userid'],), headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'})
		html = urllib2.urlopen(req).read()
		weight = re.search('<span id="weight"[^>]*>([^<]+)', html).group(1).strip().split(' ')[0]
		bmi = re.search('BMI:\s+<span id="bmi"[^>]*>([^<]+)', html).group(1).strip()
		bf = re.search('Fat:\s+<span id="bmi"[^>]*>([^<]+)', html).group(1).strip()

		msg.send('Weight: %s, BMI: %s, BF: %s' % (weight, bmi, bf))
	else:
		url = "http://wbsapi.withings.net/measure?action=getmeas&userid=%s&publickey=%s&limit=1" % (udata['userid'], udata['publickey'])
		req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'})
		obj = json.loads(urllib2.urlopen(req).read())
		meas = obj['body']['measuregrps'][0]['measures']
		weight = 'unknown'
		for m in meas:
			if m['type'] == 1:
				weight = "%.1f" % ((m['value']/1000.0)*2.20462262,)
		msg.send("Weight: %s" % weight)
