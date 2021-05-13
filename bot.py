from misc import bot, dp
import logging
import datetime as dt
import pandas as pd
import random
import asyncio
from aiogram.utils import executor

CHANNEL_NAME = -1001376231431  # HR
#CHANNEL_NAME = -1001215443026  # Test
DELAY = 60

timer_date_today = dt.time(hour=10, minute=0, second=0, microsecond=0, tzinfo=None)
timer_date = dt.time(hour=10, minute=0, second=0, microsecond=0, tzinfo=None)

db_pnti = pd.read_csv(r'PNTI.csv')
db_unti = pd.read_csv(r'UNTI.csv')
db = db_pnti.append(db_unti).reset_index()

db["Дата рождения"] = pd.to_datetime(db["Дата рождения"], format="%d.%m.%Y")

db['day'] = db['Дата рождения'].dt.day
db['month'] = db['Дата рождения'].dt.month

db = db.drop_duplicates(keep="first", ignore_index=True, subset=["Сотрудник"]).reset_index()


async def wait_until(date):
    # sleep until the specified datetime
    now = dt.datetime.now()
    await asyncio.sleep((date - now).total_seconds())


async def send_new_posts_today():
    global db
    date = dt.datetime.now()
    db_birth = db[((db["day"] == date.day) & (db["month"] == date.month))]
    if not db_birth.empty:
        post_peoples = "Уважаемые коллеги, сегодня свой день рождения отмечают:\n"

        for name, depart, status in zip(db_birth['Сотрудник'], db_birth['Подразделение'], db_birth['Должность']):
            item = str(name) + ' (' + str(depart) + ', ' + str(status) + ')' + '\n'
            post_peoples += item
        post_peoples += "\n{}".format("С днем рождения! С наилучшими пожеланиями, Ваш HR! ❤️")

        await bot.send_message(CHANNEL_NAME, post_peoples)
        await bot.send_sticker(CHANNEL_NAME, "CAACAgIAAxkBAAEB4StgJ6YzR_4j_H88wBHtKIVB9xMBMQACrQkAAnlc4gnGTO4AAVwKVRoeBA")
        logging.info('[App] Send birth today\n')
    else:
        logging.info('[App] No birth today\n')


async def periodic_birth(date):
    while True:
        await wait_until(date)
        await send_new_posts_today()
        date += dt.timedelta(days=1)

if __name__ == '__main__':
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')
    logging.info('[App] Start bot.')

    loop = asyncio.get_event_loop()

    date = dt.datetime.now()
    date = dt.datetime(year=date.year, month=date.month, day=date.day,
                       hour=timer_date.hour, minute=timer_date.minute,
                       second=timer_date.second, microsecond=timer_date.microsecond)
    loop.create_task(periodic_birth(date))

    #loop.call_later(DELAY, repeat, send_new_posts_today, loop) # use as timer

    executor.start_polling(dp, loop=loop)
    logging.info('[App] Script exited.\n')
