import requests
import logging
import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bot_token = os.environ.get('BOT_TOKEN')
pyload_address = os.environ.get('PYLOAD_ADDRESS')
pyload_username = os.environ.get('PYLOAD_USERNAME')
pyload_password = os.environ.get('PYLOAD_PASSWORD')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text='Hello! Send me a link and I will add it to Pyload.')

def add(name, link):
    payload={'username':pyload_username ,'password':pyload_password}
    with requests.session() as s: 
        r=s.post("{}/api/login".format(pyload_address), data=payload)
        print(r.text)
        payload={'name':name ,'links':[link,]}
        payloadJSON = {k: json.dumps(v) for k, v in payload.items()}
        r = s.post("{}/api/addPackage".format(pyload_address), data=payloadJSON)
        print(r.text)
        r.close()

async def handle_message(update, context):
    chat_id = update.message.chat_id
    message = update.message.text.split()
    if len(message) < 2:
        await context.bot.send_message(chat_id=chat_id, text='Please be sure to include a name for the package.')
        return

    name = message[0]
    link = message[1]
    if link.startswith('http'):
        try:
            add(name, link)
        except Exception as e:
            logging.error(e)
            await context.bot.send_message(chat_id=chat_id, text='Please send a valid link.')
            return

        await context.bot.send_message(chat_id=chat_id, text='Link added to Pyload.')
    else:
        await context.bot.send_message(chat_id=chat_id, text='Please send a valid link.')

if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    test_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(start_handler)
    application.add_handler(test_handler)

    application.run_polling()