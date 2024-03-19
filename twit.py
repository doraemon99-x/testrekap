import os
import re
import sys
from pathlib import Path

import bs4
import requests
import telebot
from tqdm import tqdm

TOKEN = '6529702195:AAFuDZiOiOXh116Ohsg3wxI86_ymDmUZQYc'
bot = telebot.TeleBot(TOKEN)

# Fungsi download_video dan download_twitter_video Anda di sini

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya adalah bot Twitter Video Downloader. Kirimkan saya URL video Twitter dan saya akan mengunduhnya untuk Anda.")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    url = message.text
    if url:
        file_path = download_twitter_video(url)
        with open(file_path, 'rb') as video:
            bot.send_video(message.chat.id, video)
    else:
        bot.reply_to(message, "URL video Twitter tidak valid.")

bot.polling()
