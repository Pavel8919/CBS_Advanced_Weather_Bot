import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Здоров! Напиши мені назву міста щоб отримати погодні дані!")


@dp.message_handler()
async def get_weather(message: types.Message):
    weather_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B",
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in weather_smile:
            wd = weather_smile[weather_description]
        else:
            wd = "Рідке погодне увище! Поглянь у вікно!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        day_length = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - \
                     datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f"Погода в місті: {city}\nТемпература: {cur_weather} °C ---> {wd}\n"
              f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст.\nВітер: {wind} м/c\n"
              f"Схід сонця: {sunrise_timestamp}\n"
              f"Захід сонця: {sunset_timestamp}\n"
              f"Тривалість дня: {day_length}"
              )

    except:
        await message.reply("\U00002757 Перевірте назву міста! \U00002757")


if __name__ == '__main__':
    executor.start_polling(dp)
