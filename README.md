# slackroon

We do it big.

To run this you need to install the requirements:

`% pip install -r pip.requirements`

Then create config.json file in the same directory as the sources. It should look something like:

```{
	"token": "<SLACK TOKEN>",
	"erruser": "<Username to send errors to>",
	"twitter": {
		"consumer_key": "XXX",
		"consumer_secret": "XXX",
		"access_token": "XXX",
		"access_token_secret": "XXX"
	},
	"weather": {
		"key": "<wunderground api key>"
	},
	"weight": {
		"users": {
			"someone": {
				"type": "fitbit",
				"userid": "XXX"
			},
			"someoneelse": {
				"type": "withings",
				"userid": "XXX",
				"publickey": "XXX"
			}
		}
	}
}```

Finally, you can execute:

`% python run.py`
