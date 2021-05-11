from telegram.ext import Updater, CommandHandler
import requests
from datetime import datetime


def start(update, context):
    """Inform user about what this bot can do"""
    update.message.reply_text(
        "Hey! How's there?\n To get status of vaccination in your area\n send me a message as */pin YOUR_PIN_CODE* \n *eg. '/pin 411030'*", parse_mode='markdown')


def Pin(update, context):
    pin = context.args
    if not pin:
        update.message.reply_text('Wrong request! Please send message like /pin YOUR_PIN_CODE \n eg. /pin 411030')
        return
    pin = context.args[0]
    today = datetime.today().strftime('%d-%m-%Y')
    uri = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={today}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    data = requests.get(uri, headers=headers)
    data = data.json()
    data = data.get('centers')
    line = ''
    indx = 1
    for rec in data:
        if rec.get('sessions')[0].get('available_capacity') == 0:
            available_capacity = ' _| Availability : 0_'
        else:
            ct = str(rec.get('sessions')[0].get('available_capacity'))
            available_capacity = f' *| Availability : {ct}*'
        line += str('\n') + str(indx) + '. Center Name : ' + rec.get('name') + ' | Age Group : ' + str(
            rec.get('sessions')[0].get('min_age_limit')) + available_capacity
        indx += 1
    if line:
        update.message.reply_text(line, parse_mode='markdown')
    else:
        update.message.reply_text('No Vaccination center is available for booking!')


def main():
    updater = Updater('API_KEY', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('Pin', Pin))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

