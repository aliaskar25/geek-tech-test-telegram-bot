import os

HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", default='geek-tech-telegram-bot')

WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com/'
WEBHOOK_PATH = f'/webhook/{os.getenv("BOT_TOKEN", "5663202583:AAE78paT0RNgDmNSxvw1zNfIYbzJ-w3yri0")}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8000
