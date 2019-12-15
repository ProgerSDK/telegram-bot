# telegram-bot

This repository contains a test bot for the telegram. The bot is written in python using the [Telegram Bot API](https://core.telegram.org/api) and wrapper library over api [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/). To make the bot work, you need to substitute your tokens in [config.py](./bot/config.py).

## [bot](./bot/)

The folder contains main bot code.

## API

The following APIs are also used for the bot:

* [Clarifai API](https://docs.clarifai.com/)
* [Random Dog API](https://random.dog/woof.json)
* [Yes Or No API](https://yesno.wtf/#api)

## Heroku
Files [Procfile](./Procfile), [requirements.txt](./requirements.txt), [runtime.txt](./runtime.txt) are needed for Deploy on heroku. If you Deploy a bot on heroku, you need to delete the files: Pipfile, Pipfile.lock .