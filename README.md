# What is BarnameKon?
Barname Kon is telegram bot which create "Add to Calendar" link (Google Calendar) and file (.ics) for your event. It only accept Jalali date and Tehran time.

# 8K Satoshi for [this](https://github.com/anvaari/BarnameKon/issues/1) feature
I will pay 8000 Satoshi for who work on [this](https://github.com/anvaari/BarnameKon/issues/1) issue and add that feature.
I know this isn't too much. But it is amount of $btc which I can pay. I wish it encourage you :)

# Deploy on local

- Install Heroku cli [From Here](https://devcenter.heroku.com/articles/heroku-cli#download-and-install). You should change your IP for sign up [from Iran to anywhere!]
- Download [Ngrok](https://ngrok.com/download) and set it on port 5000 (`./ngrok http 5000`)
- Clone Repository 
- Create virtural env and install requirements.
- Change variable in .env.sample in proper way
    - You should create a bot in [@Botfather](https://t.me/botfather).
- Rename .env.sample to .env
- In Barnamekon.py : 
   - See [line 197](https://github.com/anvaari/BarnameKon/blob/f7a98f6166f77f2531d850d55f7c52688d491f54/BarnameKon.py#L197)
   - See [line  204 ](https://github.com/anvaari/BarnameKon/blob/f7a98f6166f77f2531d850d55f7c52688d491f54/BarnameKon.py#L204)
- `cd path/to/barnamekon`
- `heroku local web`
- open this address in your browser localhost:5000 . if `!` appear it means it deployed successfully else, see terminal for log. 
- Go to telegram and interact with Barnamekon.

**I know it isn't not a simple way but I can't find better way. If you have an idea please open issue and tell me about that, it's really appreciated.**
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


**2021/8/11** : Add .env.sample file. Also add steps to README.md for deploying Barnamekon in local machine.

# Donation
Donation make developer of this project so happy and greatful :) So if Barnamekon help you and want donate, here is my address on lightning network. You can donate bitcoin with less amount of fee :)

lightning: mohammadanvary@lntxbot.com
