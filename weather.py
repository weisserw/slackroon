from slackbot.bot import respond_to
from slackbot.bot import listen_to
 
import re
import urllib2
import json

from config import conf
 
@listen_to(r'^!w\s+([0-9]{5})')
def weather(message, zipcode):
    w = getweather(zipcode)
    message.send_webapi('', json.dumps([{
        'fallback': w,
        'text': "<https://www.wunderground.com/cgi-bin/findweather/getForecast?query=%s|%s>" % (zipcode, w),
    }]))

def getweather(zipcode):
    key = conf['weather']['key']

    url = 'http://api.wunderground.com/api/' + key + '/geolookup/conditions/q/PA/' + zipcode + '.json'

    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    f.close()

    city = parsed_json['location']['city']
    state = parsed_json['location']['state']
    weather = parsed_json['current_observation']['weather']
    temperature_string = parsed_json['current_observation']['temperature_string']
    feelslike_string = parsed_json['current_observation']['feelslike_string']
    if feelslike_string != temperature_string:
        return city + ', ' + state + ': ' + weather.lower() + ', ' + temperature_string + ', feels like ' + feelslike_string + '.'
    else:
        return city + ', ' + state + ': ' + weather.lower() + ', ' + temperature_string + '.'
