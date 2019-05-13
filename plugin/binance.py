import re
import time
from html import unescape

import requests

import telegram
from telegram.ext import run_async
from telegram.error import BadRequest


@run_async
def binance(bot, update):
    if update.message:
        if update.message.caption:
            update.message.text = update.message.caption

    if update.edited_message:
        if update.edited_message.caption:
            update.message = update.edited_message
            update.message.text = update.edited_message.caption
        else:
            update.message = update.edited_message
            update.message.text = update.edited_message.text

    pattern = '(t.cn\/)(.\w+)'
    result = re.findall(pattern, unescape(update.message.text_html))
    for x in result:
        if x:
            try:
                real_url = requests.get(f'http://t.cn/{x[1]}')
            except requests.exceptions.ConnectionError as e:
                update.message.text = f"http://{e.args[0].pool.host}"
            update.message.text = real_url.url
    if validators.url(update.message.text) != True:
        return
    pattern = '(binance|exhangecenter)'
    result = re.findall(pattern, update.message.text)
    if result:
        try:
            try:
                update.message.delete()
            except:
                pass
            bot.restrict_chat_member(update.message.chat_id, update.message.from_user.id, can_send_messages=None,
                                     can_send_media_messages=None, can_send_other_messages=None, can_add_web_page_previews=None)
        except BadRequest as e:
            if e.message == 'Not enough rights to restrict/unrestrict chat member':
                if e.message == 'Not enough rights to restrict/unrestrict chat member':
                    sent = update.message.reply_text(
                        '偵測到 <code>Spam_Binance_URL</code>\n權限不足無法正常處置(´･ω･`)', parse_mode='html').result()
                    time.sleep(10)
                    bot.delete_message(update.message.chat_id, sent.message_id)
                    return
        else:
            tmp_text = '偵測到 <code>Spam_Binance_URL</code>\n' \
                f'{update.message.from_user.mention_html()} 在和 <code>hexlightning</code> 戰鬥時被燒掉了自己的魔書，因而只能<code>永久</code>退出這場戰鬥。\n若有誤判請至 @hexjudge 申請。'
            sent = update.message.reply_text(
                tmp_text, parse_mode='html').result()
            time.sleep(10)
            bot.delete_message(update.message.chat_id, sent.message_id)

        try:
            bot.kick_chat_member(update.message.chat_id,
                                 update.message.from_user.id)
        except BadRequest as e:
            sent = update.message.reply_text(
                '偵測到 <code>Spam_Binance_URL</code>\n權限不足無法正常處置(´･ω･`)', parse_mode='html').result()
            time.sleep(5)
            bot.delete_message(update.message.chat_id, sent.message_id)
