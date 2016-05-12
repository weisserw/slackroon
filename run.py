#!/usr/bin/env python

import logging
logging.basicConfig()

from slackbot.bot import Bot

def main():
	bot = Bot()
	bot.run()

if __name__ == "__main__":
	main()
