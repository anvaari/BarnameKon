
"""
Created on Mon Feb  1 22:41:45 2021

@author: anvaari
"""


import telebot
from flask import Flask,request
import os


from urllib.parse import quote as urldecode
from datetime import datetime  as dt
from datetime import timedelta
from jdatetime import datetime  as jdt 
from dateutil import tz
from ics import Event,Calendar

def evligen(title,start_datetime,end_datetime,location,discription):
    '''
    This Function get data about event and return url for publish event and ics object

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
    tuple
        Url for publishing event, calendar object

    '''
    c=Calendar()
    e=Event()
    e.name=title
    e.description=discription
    e.location=location
    
    main_url='https://calendar.google.com/calendar/render?action=TEMPLATE&dates={}%2F{}&details={}&location={}&text={}' #for create link we must use this format
    title=urldecode(title)
    location=urldecode(location)
    discription=urldecode(discription)
    
    start_datetime=jdt.strptime(start_datetime,"%Y/%m/%d-%H:%M").togregorian()
    start_datetime=dt(start_datetime.year,start_datetime.month,start_datetime.day,start_datetime.hour,start_datetime.minute) # Convert to datetime object because JalaliDateTime use earlier version of datetime and in that version timezone don't work properly.
    start_datetime=start_datetime.replace(tzinfo=tz.gettz('Iran')).astimezone(tz=tz.gettz('UTC'))
    e.begin=start_datetime.strftime("%Y-%m-%d %H:%M:%S")
    start_datetime-=timedelta(minutes=4) # This -4 use when deploy in heroku. I don't know why in kerkulo it show converted time with extera 4 minute.
    # Solve summer time
    if (start_datetime.month>=4 or (start_datetime.month==3 and start_datetime.day>=22)) and (start_datetime.month<=8 or (start_datetime.month==9 and start_datetime.day<=22)): 
        start_datetime=dt(start_datetime.year,start_datetime.month,start_datetime.day,start_datetime.hour-1,start_datetime.minute) 
    start_datetime=start_datetime.strftime("%Y%m%dT%H%M%SZ") # Google calendar only accept this format.
    
    end_datetime=jdt.strptime(end_datetime,"%Y/%m/%d-%H:%M").togregorian()
    end_datetime=dt(end_datetime.year,end_datetime.month,end_datetime.day,end_datetime.hour,end_datetime.minute)
    end_datetime=end_datetime.replace(tzinfo=tz.gettz('Iran')).astimezone(tz=tz.gettz('UTC'))
    e.end=end_datetime.strftime("%Y-%m-%d %H:%M:%S")
    end_datetime-=timedelta(minutes=4)
    # Solve summer time
    if (end_datetime.month>=4 or (end_datetime.month==3 and end_datetime.day>=22)) and (end_datetime.month<=8 or (end_datetime.month==9 and end_datetime.day<=22)): 
        end_datetime=dt(end_datetime.year,end_datetime.month,end_datetime.day,end_datetime.hour-1,end_datetime.minute) 
    end_datetime=end_datetime.strftime("%Y%m%dT%H%M%SZ")
    
    
    
    c.events.add(e)
    
    return main_url.format(start_datetime,end_datetime,discription,location,title),c



def feed_info_to_evligen(mes_text):
    '''
    This Function get text message entered by user and prepare it  to feed in evligen function

    Parameters
    ----------
    mess_text : str
    	it must have special formated which mentioned in bot for user.

    Returns
    -------
    tuple
        Url for publishing event generated for input message, calendar object for creating ics file

    '''
    
    mes_text=mes_text.split('\n')
    event_link=evligen(mes_text[1],mes_text[3],mes_text[4],mes_text[2],'\n'.join(mes_text[5:]))
    return event_link

    
heroku_app_name='{}'.format(os.environ.get('h_a_n')) #Find it in  your heruko dashboard
log_chat_id= int(os.environ.get('l_c_i'))  #Chat Id which you want store log there
token = '{}'.format(os.environ.get('bot_token')) #Give it from @BotFather (Telegram)
bot=telebot.TeleBot(token)


sample_event_txt='رویداد\nمقدمه ای بر مصورسازی داده در پایتون\nskyroom\n1399/11/18-17:00\n1399/11/18-19:00\nبرای مشاهده رویداد در ساعت شروع آن به ادرس زیر مراجعه کنید:‌\nhttps://skyroom.online/datavisual'
sample_event=feed_info_to_evligen(sample_event_txt)
sample_event_link=sample_event[0]
sample_event_cal=sample_event[1]

# This part use for deploying
server = Flask(__name__)
PORT = int(os.environ.get('PORT', '8443'))
  

# Handle 'start' command
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "سلام :) \n من (برنامه کُن!) اینجا هستم تا بتونی رویداد هایی رو که میبینی به تقویم هات اضافه کنی.\n برای اینکه بدونی چطوری کار میکنم /help رو وارد کن.")
    bot.send_sticker(message.chat.id,'CAACAgQAAxkBAANKYCDnIB96YtMVvksVg9J5rCHu_lEAAtoBAAIhiDAI59nW5NwpahkeBA')
    if message.chat.type == 'private':
        bot.send_message(log_chat_id,'@{} Start. ID: {}\n'.format(message.from_user.username,message.chat.id))
    else:
        bot.send_message(log_chat_id,'@{} Start in {} group @{}\n'.format(message.from_user.username,message.chat.title,message.chat.username))


# Handle 'help' command
@bot.message_handler(commands=['help'])
def handle_help(message):
    if message.chat.type=='private':
        bot.send_message(message.chat.id,'برای دریافت لینک اضافه کردن به تقویم گوگل و فایل ics رویداد اطلاعات رویداد رو به فرمت زیر برای من بفرست:')
        bot.send_message(message.chat.id,'رویداد \nعنوان رویداد\nمکان رویداد\nزمان و تاریخ شروع به فرمت پیام بعد\nزمان و تاریخ پایان به فرمت پیام بعد\nتوضیحات رویداد (شامل لینک و باقی توضیحات)')
        bot.send_message(message.chat.id,sample_event_txt)
        bot.send_message(message.chat.id,f'لینک اضافه کردن رویداد نمونه بالا به تقویم گوگل  : \n{sample_event_link}')
        with open('Your_Event.ics','w') as fp:
            fp.writelines(sample_event_cal)
        with open('Your_Event.ics','rb') as fp:
            bot.send_message(message.chat.id,'فایل ics این رویداد ')
            bot.send_document(message.chat.id, fp)
    else:
        bot.send_message(message.chat.id,'برای دریافت لینک اضافه کردن به تقویم گوگل و فایل ics رویداد اطلاعات رویداد رو به فرمت زیر به همین پیام Reply بزن :)')
        bot.send_message(message.chat.id,'رویداد \nعنوان رویداد\nمکان رویداد\nزمان و تاریخ شروع به فرمت پیام بعد\nزمان و تاریخ پایان به فرمت پیام بعد\nتوضیحات رویداد (شامل لینک و باقی توضیحات)')
        bot.send_message(message.chat.id,sample_event_txt)
        bot.send_message(message.chat.id,f'لینک اضافه کردن رویداد نمونه بالا به تقویم گوگل  : \n{sample_event_link}')
        with open('Your_Event.ics','w') as fp:
            fp.writelines(sample_event_cal)
        with open('Your_Event.ics','rb') as fp:
            bot.send_message(message.chat.id,'فایل ics این رویداد ')
            bot.send_document(message.chat.id, fp)

# Handle text message   
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if 'رویداد' in message.text : 
        try:
            if message.chat.type=='private':
                event=feed_info_to_evligen(message.text)
                calendar=event[1]
                event_link=event[0]
                bot.send_message(message.chat.id,f'لینک رویداد شما :\n{event_link}')
                with open('Your_Event.ics','w') as fp:
                    fp.writelines(calendar)
                with open('Your_Event.ics','rb') as fp:
                    bot.send_message(message.chat.id,'فایل ics رویداد شما')
                    bot.send_document(message.chat.id, fp)
                bot.send_message(log_chat_id,'@{} Create Link. ID: {}\n'.format(message.from_user.username,message.chat.id))


            else:
                event=feed_info_to_evligen(message.text)
                calendar=event[1]
                event_link=event[0]               
                bot.reply_to(message,f'لینک رویداد شما :\n{event_link}')
                with open('Your_Event.ics','w') as fp:
                    fp.writelines(calendar)
                with open('Your_Event.ics','rb') as fp:
                    bot.send_message(message.chat.id,'فایل ics رویداد شما')
                    bot.send_document(message.chat.id, fp)
                bot.send_message(log_chat_id,'@{} Create Link in {} group @{}\n'.format(message.from_user.username,message.chat.title,message.chat.username))
        except:
            bot.send_message(message.chat.id,"غالب اطلاعات ارسالی درست نیست. لطفا یه نگاهی به راهنمای برنامه کُن بنداز : /help")
          
    else:
        bot.send_message(message.chat.id,"غالب اطلاعات ارسالی درست نیست. لطفا یه نگاهی به راهنمای برنامه کُن بنداز : /help")
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


