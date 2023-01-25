from movies_scraper import search_movies, get_movie
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request
import requests
from queue import Queue
from io import BytesIO
import os

TOKEN = os.getenv("TOKEN")
URL = 'https://mega-mov.vercel.app'
bot = Bot(TOKEN)


def welcome(update, context) -> None:
    update.message.reply_text(f"Hey {update.message.from_user.first_name}, Welcome to MegaMov\n"
                              f"A one platform place for all Movies")
    update.message.reply_text("Start by searching a movie")
    
def trending(update, context) -> None:
    update.message.reply_text("We are working on this feature..\nTo be updated soon")


def find_movie(update, context):
    search_results = update.message.reply_text("Processing")
    query = update.message.text
    movies_list = search_movies(query)
    if movies_list:
        keyboards = []
        for movie in movies_list:
            keyboard = InlineKeyboardButton(
                movie["title"], callback_data=movie["id"])
            keyboards.append([keyboard])
        reply_markup = InlineKeyboardMarkup(keyboards)
        search_results.edit_text(
            'Look what I\'ve found', reply_markup=reply_markup)
    else:
        search_results.edit_text(
            'Sorry, No Results Found!\nCheck the Movie name you\'ve typed')


def movie_result(update, context) -> None:
    query = update.callback_query
    s = get_movie(query.data)
    response = requests.get(s["img"])
    img = BytesIO(response.content)
    query.message.reply_photo(photo=img, caption=f"🎥 {s['title']}")
    link = ""
    links = s["links"]
    for i in links:
        link += "🎬" + i + "\n" + links[i] + "\n\n"
    caption = f"⚡ Fast Download Links :-\n\n{link}"
    if len(caption) > 4095:
        for x in range(0, len(caption), 4095):
            query.message.reply_text(text=caption[x:x+4095])
    else:
        query.message.reply_text(text=caption)


def setup():
    update_queue = Queue()
    dispatcher = Dispatcher(bot, update_queue, use_context=True)
    dispatcher.add_handler(CommandHandler('start', welcome))
    dispatcher.add_handler(CommandHandler('trending', trending))
    dispatcher.add_handler(MessageHandler(Filters.text, find_movie))
    dispatcher.add_handler(CallbackQueryHandler(movie_result))
    return dispatcher


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    setup().process_update(update)
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
