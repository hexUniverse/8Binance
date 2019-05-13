from telegram.ext.dispatcher import run_async


@run_async
def ping(bot, update):
    update.message.reply_text('pong')
