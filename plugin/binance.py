import re
import time
from html import unescape

import requests
import validators

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
                req = requests.get(
                    f'http://t.cn/{x[1]}', allow_redirects=False)
                real_url = req.headers['Location']
            except requests.exceptions.ConnectionError as e:
                update.message.text = f"http://{e.args[0].pool.host}"
            else:
                # if real_url.status_code != 200:
                #    return
                update.message.text = real_url
    ### EXTRACT URL ###
    pattern = '((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)'
    extrac = re.findall(pattern, update.message.text)
    ### EXTRACT URL ###
    for url in extrac:
        update.message.text = url
        if validators.url(update.message.text) != True:
            return
        pattern = '(binance|exhangecenter|marketrelease)'
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
                        bot.delete_message(
                            update.message.chat_id, sent.message_id)
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
