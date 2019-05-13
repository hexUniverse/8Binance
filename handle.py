__author__ = '@DingChen_Tsai'

# python-telegeam-bot
import telegram.bot
from telegram import user
from telegram.error import *
from telegram.utils.request import Request
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Filters, messagequeue

import logging
import time
import asyncio

# Custom
from command import ping, error
from plugin import binance


class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or messagequeue.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @messagequeue.queuedmessage
    def send_message(self, *args, **kwargs):
        """Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments"""
        try:
            return super(MQBot, self).send_message(*args, **kwargs)
        except (BadRequest, TimedOut, Unauthorized) as e:
            if e.message == 'Reply message not found':
                #logger.warning('msg has deleted.')
                kwargs.pop('reply_to_message_id', None)
                return super(MQBot, self).send_message(*args, **kwargs)
            elif e.message == 'Timed out':
                logger.warning('Timed out.')
            elif e.message == "Forbidden: bot can't initiate conversation with a user":
                logger.warning('cannot reach that guys')
            elif e.message == 'Forbidden: bot is not a member of the supergroup chat':
                logger.warning('new left from group')
                # raise

            else:
                logger.exception(e)
                logger.warning(args)
                logger.warning(kwargs)


def worker(inherit, **kwargs):
    global logger
    # app = command.app(inherit)
    token = kwargs['token']

    # for test purposes limit global throughput to 30 messages per 2 sec
    q = messagequeue.MessageQueue(all_burst_limit=2, all_time_limit_ms=3000)
    request = Request(con_pool_size=14)
    bot = MQBot(token, request=request, mqueue=q)
    updater = Updater(
        bot=bot,
        workers=10)

    # get the dispatcher to register handlers
    dp = updater.dispatcher
    logger = inherit.logger
    logger = logging.getLogger(__name__)
    logger.info(f'{bot.get_me().first_name} is listening...')

    # set handle #
    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(MessageHandler(
        (Filters.text | Filters.photo) & Filters.group, binance, edited_updates=True))
    dp.add_error_handler(error)

    try:
        updater.start_polling(clean=False)
        updater.idle()
    except KeyboardInterrupt:
        updater.stop()
        updater.is_idle = False
