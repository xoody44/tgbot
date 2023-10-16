import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink, hide_link
from aiogram.dispatcher.filters import Text
from config import token, user_id
from p123 import check_news_update


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Лента новостей", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f"{hide_link(v['article_image'])}" \
               f"{hbold(v['article_date'])}\n" \
               f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news, parse_mode=types.ParseMode.HTML)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hide_link(v['article_image'])}" \
                   f"{hbold(v['article_date'])}\n" \
                   f"{hlink(v['article_title'], v['article_url'])}"

            await message.answer(news, parse_mode=types.ParseMode.HTML)

    else:
        await message.answer("Пока нет свежих новостей")


async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hide_link(v['article_image'])}" \
                       f"{hbold(v['article_date'])}\n" \
                       f"{hlink(v['article_title'], v['article_url'])}"

                # id @userinfobot
                await bot.send_message(user_id, news, disable_notification=True, parse_mode=types.ParseMode.HTML)

        #else:
        #    await bot.send_message(user_id, "Пока нет свежих новостей...", disable_notification=True)

        await asyncio.sleep(360)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)