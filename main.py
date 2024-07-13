import telethon
import asyncio
import re
import requests
from telethon import TelegramClient, events
from random_address import real_random_address
import names
from datetime import datetime
import random
from defs import getUrl, getcards, phone
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = #api id
API_HASH = 'Api Hash'
BOT_TOKEN = '7397315889:AAGFhr7kQAZ_BPLHl8Puc3sf-FjPdbBlKmc'
SEND_CHAT = '@scrapperprodex'

client = TelegramClient('session', API_ID, API_HASH)
bot = telebot.TeleBot(BOT_TOKEN)
ccs = []

chats = [
    '@BlackHeadscc',
    '@b3approved',
    '@BINCCLive',
    '@JLScrapper',
    '@Good_Charge_Scrapper_Chat'
]

with open('cards.txt', 'r') as r:
    temp_cards = r.read().splitlines()

for x in temp_cards:
    car = getcards(x)
    if car:
        ccs.append(car[0])

@client.on(events.NewMessage(chats=chats, func=lambda x: getattr(x, 'text')))
async def my_event_handler(m):
    if m.reply_markup:
        text = m.reply_markup.stringify()
        urls = getUrl(text)
        if not urls:
            return
        text = requests.get(urls[0]).text
    else:
        text = m.text
    cards = getcards(text)
    if not cards:
        return
    cc, mes, ano, cvv = cards
    if cc in ccs:
        return
    ccs.append(cc)
    bin_response = requests.get(f'https://api.dlyar-dev.tk/info-bin?bin={cc[:6]}')
    if not bin_response:
        return
    bin_json = bin_response.json()
    addr = real_random_address()
    fullinfo = (f"{cc}|{mes}|{ano}|{cvv}|{names.get_full_name()}|{addr['address1']}|{addr['city']}|"
                f"{addr['state']}|{addr['postalCode']}|{phone()}|dob: {datetime.strftime(datetime(random.randint(1960, 2005), random.randint(1, 12), random.randint(1, 28)), '%Y-%m-%d')}|United States Of America")

    text = (f"Approved ✅\n\nCard -> `{cc}|{mes}|{ano}|{cvv}`\n━━━━━━━━━━━━━━━\nBin Info \n-> {bin_json['bin']}\n-> {bin_json['scheme']}\n-> {bin_json['type']}\n-> {bin_json['brand']}\n-> {bin_json['bank']}\n-> {bin_json['country']} {bin_json['flag']}\n━━━━━━━━━━━━━━━\nAdditional Information\n\n-> {fullinfo}")

    print(f'{cc}|{mes}|{ano}|{cvv}')
    with open('cards.txt', 'a') as w:
        w.write(fullinfo + '\n')
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Developer", url="t.me/Dexter_ffx"),
        InlineKeyboardButton("Coder", url="t.me/SandeepKhadka7"),
        InlineKeyboardButton("Youtube", url="t.me/its_OldDexter")
    )

    bot.send_message(SEND_CHAT, text, reply_markup=markup, parse_mode='Markdown')

@client.on(events.NewMessage(outgoing=True, pattern=re.compile(r'[./!]extrap( (.*))')))
async def extrap_handler(m):
    text = m.pattern_match.group(1).strip()
    with open('cards.txt', 'r') as r:
        cards = r.read().splitlines() # list of cards
    if not cards:
        return await m.reply("Not Found")
    r = re.compile(f"{text}*.")
    if not r:
        return await m.reply("Not Found")
    newlist = list(filter(r.match, cards)) # Read Note below
    if not newlist:
        return await m.reply("Not Found")
    if len(newlist) == 0:
        return await m.reply("0 Cards found")
    cards = "\n".join(newlist)
    return await m.reply(cards)

@client.on(events.NewMessage(outgoing=True, pattern=re.compile(r'.lives')))
async def lives_handler(m):
    await m.reply(file='cards.txt')

client.start()
client.run_until_disconnected()
