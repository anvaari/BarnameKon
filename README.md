# What is BarnameKon?
Barname Kon is telegram bot which create "Add to Calendar" link (Google Calendar) and file (.ics) for your event. It only accept Jalali date and Tehran time.


# How can I create my bot? 
I use [this](https://medium.com/better-programming/how-to-create-telegram-bot-in-python-cccc4babcc30) medium post and [official pyTelegramBOTAPI documents](https://github.com/eternnoir/pyTelegramBotAPI)


# How can I deploy my bot ?
I think fast,best and cheapest 😁 way for deploy your Bot is heroku.
[This post](https://github.com/devskrate/dev/blob/79f913fd55eb83f4d9b68d5e4b42ee2e40566c65/_posts/2020-02-18-simple-python-telegram-bot.md) really help me to do that.

# How to contribute to BarnameKon?
I oppened two issue that explain my ideas for improving this project. So feel free to send pull request or open new issue.  

# Updates 
**2021/3/29** : Solve the problem of summer time. (Barnamekon set time 1 hour ahead when summer time come.)

**2021/5/19** : Create ics file for events. But ics file don't show time correctly (I think this is the problem with timezone), It will be fixed in next update.


**2021/6/3** : Bug related to pytz library and [known bug](https://icspy.readthedocs.io/en/stable/misc.html#datetimes-are-converted-to-utc-at-parsing-time) from ics library which incorrectly set time in ics file, fixed.