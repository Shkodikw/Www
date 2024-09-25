import requests 
import datetime 
import telebot 
from telebot import types 
 
API_KEY = '6695254684:AAGX_Doc3bcePztB1U9ns_9EqmR182HbYCc' 
WEATHER_API_KEY = '9de8c4351b766464c549cf2a5dabdb7e' 
bot = telebot.TeleBot(API_KEY) 
 
@bot.message_handler(commands=["start"]) 
def start_command(message: types.Message): 
    bot.reply_to(message, "Привет! Напиши мне название города и я пришлю сводку погоды!") 
 
@bot.message_handler(func=lambda message: True) 
def get_weather(message: types.Message): 
    code_to_smile = { 
        "Clear": "Ясно \U00002600", 
        "Clouds": "Облачно \U00002601", 
        "Rain": "Дождь \U00002614", 
        "Drizzle": "Дождь \U00002614", 
        "Thunderstorm": "Гроза \U000026A1", 
        "Snow": "Снег \U0001F328", 
        "Mist": "Туман \U0001F32B" 
    } 
 
    try: 
        r = requests.get( 
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_API_KEY}&units=metric" 
        ) 
        data = r.json() 
 
        city = data["name"] 
        cur_weather = data["main"]["temp"] 
 
        weather_description = data["weather"][0]["main"] 
        wd = code_to_smile.get(weather_description, "Посмотри в окно, не пойму что там за погода!") 
 
        humidity = data["main"]["humidity"] 
        wind = data["wind"]["speed"] 
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]) 
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) 
        length_of_the_day = sunset_timestamp - sunrise_timestamp 
 
        bot.reply_to(message, f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n" 
                              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n" 
                              f"Влажность: {humidity}%\nВетер: {wind} м/с\n" 
                              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n" 
                              f"Продолжительность дня: {length_of_the_day}\n" 
                              f"***Хорошего дня!***") 
 
    except Exception as e: 
        bot.reply_to(message, "\U00002620 Проверьте название города \U00002620") 
 
if name == '__main__': 
    bot.polling(none_stop=True)