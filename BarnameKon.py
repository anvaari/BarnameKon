#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 22:41:45 2021

@author: anvaari
"""


import telebot
from flask import Flask,request
import os


from urllib.parse import quote as urldecode
from datetime import datetime  as dt
from jdatetime import datetime  as jdt 
from pytz import timezone

def evligen(title,start_datetime,end_datetime,location,discription):
    '''
    This Function get data about event and return url for publish event

    Parameters
    ----------
    title : str
        Title of event.
    start_datetime : str
        start date and time of envent in Jalali calendar. accepted format is : {Year}{Month}{Day}T{Hour}{Minute}
    end_datetime : str
        end date and time of envent in Jalali calendar. accepted format is : {Year}{Month}{Day}T{Hour}{Minute}
    location : str
        Location of event.
    discription : str
        Detail of event such as address of other info.

    Returns
    -------
    str
        Url for publishing event.

    '''
    
    main_url='https://calendar.google.com/calendar/render?action=TEMPLATE&dates={}%2F{}&details={}&location={}&text={}' #for create link we must use this format
    title=urldecode(title)
    location=urldecode(location)
    discription=urldecode(discription)
    
    start_datetime=jdt.strptime(start_datetime,"%Y/%m/%d-%H:%M").togregorian()
    start_datetime=dt(start_datetime.year,start_datetime.month,start_datetime.day,start_datetime.hour,start_datetime.minute) # Convert to datetime object because JalaliDateTime use earlier version of datetime and in that version timezone don't work properly.
    start_datetime=start_datetime.replace(tzinfo=timezone('Iran')).astimezone(tz=timezone('UTC'))
    start_datetime=dt(start_datetime.year,start_datetime.month,start_datetime.day,start_datetime.hour,start_datetime.minute-4)# This -4 use when deploy in heroku. I don't know why in kerkulo it show converted time with extera 4 minute.
    start_datetime=start_datetime.strftime("%Y%m%dT%H%M%SZ") # Google calendar only accept this format.
    
    end_datetime=jdt.strptime(end_datetime,"%Y/%m/%d-%H:%M").togregorian()
    end_datetime=dt(end_datetime.year,end_datetime.month,end_datetime.day,end_datetime.hour,end_datetime.minute)
    end_datetime=end_datetime.replace(tzinfo=timezone('Iran')).astimezone(tz=timezone('UTC'))
    end_datetime=dt(end_datetime.year,end_datetime.month,end_datetime.day,end_datetime.hour,end_datetime.minute-4)
    end_datetime=end_datetime.strftime("%Y%m%dT%H%M%SZ")
    
    
    return main_url.format(start_datetime,end_datetime,discription,location,title)



def feed_info_to_evligen(mes_text):
    '''
    This Function get text message entered by user and prepare it  to feed in evligen function

    Parameters
    ----------
    mess_text : str
    	it must have special formated which mentioned in bot for user.

    Returns
    -------
    list
        Url for publishing event generated for input message.

    '''
    
    mes_text=mes_text.split('\n')
    event_link=evligen(mes_text[0],mes_text[2],mes_text[3],mes_text[1],'\n'.join(mes_text[4:]))
    return event_link

    
heroku_app_name='' #Find it in  your heruko dashboard
token = '' #Get it from @BotFather (Telegram)
bot=telebot.TeleBot(token)


sample_event='رویداد\nمقدمه ای بر مصورسازی داده در پایتون\nskyroom\n1399/11/18-17:00\n1399/11/18-19:00\nبرای مشاهده رویداد در ساعت شروع آن به ادرس زیر مراجعه کنید:‌https://skyroom.ir/datavisual'
sample_event_link=feed_info_to_evligen(sample_event)

# This part use for deploying
server = Flask(__name__)
PORT = int(os.environ.get('PORT', '8443'))
  

# Handle 'start' command
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "سلام :) \n من (برنامه کُن!) اینجا هستم تا بتونی رویداد هایی رو که میبینی به تقویم گوگلت اضافه کنی.\n برای اینکه بدونی چطوری کار میکنم /help رو وارد کن.")
    bot.send_sticker(message.chat.id,'CAACAgQAAxkBAANKYCDnIB96YtMVvksVg9J5rCHu_lEAAtoBAAIhiDAI59nW5NwpahkeBA')

# Handle 'help' command
@bot.message_handler(commands=['help'])
def handle_help(message):
    if message.chat.type!='group':
        bot.send_message(message.chat.id,'برای دریافت لینک رویداد اطلاعات رویداد رو به فرمت زیر بفرست:')
        bot.send_message(message.chat.id,'رویداد \nعنوان رویداد\nمکان رویداد\nزمان و تاریخ شروع به فرمت پیام بعد\nزمان و تاریخ پایان به فرمت پیام بعد\nتوضیحات رویداد (شامل لینک و باقی توضیحات)')
        bot.send_message(message.chat.id,sample_event)
        bot.send_message(message.chat.id,f'لینک رویداد نمونه بالا : \n{sample_event_link}')

        

# Handle text message   
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if 'رویداد' in message.text : 
        try:
            event_link=feed_info_to_evligen(message.text)
            bot.send_message(message.chat.id,f'لینک رویداد شما :\n{event_link}')
        except:
            bot.send_message(message.chat.id,"غالب اطلاعات ارسالی درست نیست. لطفا یه نگاهی به راهنمای رباتبنداز : /help")
          
    else:
        bot.send_message(message.chat.id,"غالب اطلاعات ارسالی درست نیست. لطفا یه نگاهی به راهنمای رباتبنداز : /help")
# Handle sticker message   
@bot.message_handler(content_types=['sticker'])
def handle_stickers(message):
    bot.send_message(message.chat.id,'این یکی بهتره ;)')
    bot.send_sticker(message.chat.id,'CAACAgQAAxkBAANKYCDnIB96YtMVvksVg9J5rCHu_lEAAtoBAAIhiDAI59nW5NwpahkeBA')


# This part use for deploying   
@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://{heroku_app_name}.herokuapp.com/' + token)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


