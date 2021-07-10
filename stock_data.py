import requests
import telebot
import logging
from datetime import datetime

bot_token = "YOUR_API_KEY"
bot = telebot.TeleBot(token = bot_token, parse_mode = "HTML")

token = "YOUR_IEX_CLOUD_API_KEY"

api_url = "https://cloud.iexapis.com/stable/stock"

def get_stock_quote(stock):
    r = requests.get(url = f'{api_url}/{stock}/quote?token={token}')
    data = r.json()
    return f'<b>Ticker</b>: ${data["symbol"]}\n<b>Open</b>: {data["open"]}\n<b>Close</b>: {data["close"]}\n<b>Volume</b>: {data["latestVolume"]:,}\n<b>RH Price</b>: {data["latestPrice"]}\n<b>RH Change</b>: {round(data["changePercent"]*100, 2)}%\n<b>AH Price</b>: {data["extendedPrice"]}\n<b>AH Change</b>: {round(data["extendedChangePercent"]*100,2)}%\n\n'

def get_news(stock):
    r = requests.get(url = f'{api_url}/{stock}/news/last/3?token={token}')
    data = r.json()
    list_of_articles = ""
    for news in data:
        list_of_articles += "<b>Title:</b> " + news["headline"] + "\n" + "<b>Source:</b> " + news["source"] + "\n" + "Date: " + str(datetime.fromtimestamp(news["datetime"]/1000.0)) + "\n<a href = '" + news["url"] + "'>Link</a>" + "\n\n"  
    return list_of_articles

@bot.message_handler(commands=['start'])
def handle_command(message):
    bot.reply_to(message, "Hi, send me a ticker! \U0001F680 \U0001F680 \U0001F680")

@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    if(message.text[0] == '$'):
       try:
            full_quote = get_stock_quote(message.text[1:]) + get_news(message.text[1:])
            bot.reply_to(message, full_quote, disable_web_page_preview=True)
       except Exception as e:
            bot.reply_to(message, "There was an error, please try again")
            logging.error(traceback.format_exc())

bot.polling()