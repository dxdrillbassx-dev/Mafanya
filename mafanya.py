import discord
from discord.ext import commands
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import requests
from io import BytesIO
from PIL import Image
import re
import os
import numpy as np
import random
import json

from weather import get_weather  # Импортируем функцию для работы с погодой
from train_data import train_data  # Импортируем переменную train_data
from image_handling import image_urls, send_image  # Импортируем переменную image_urls и функцию send_image
from image_handling import on_message as image_on_message

# Предполагается, что у вас есть файл config.py с содержимым:
# token = 'ВАШ_ТОКЕН_BOT'
# weather_api_key = 'ВАШ_API_КЛЮЧ'
import config

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

classifier = MultinomialNB()
vectorizer = CountVectorizer()

# Добавляем функционал для сохранения истории сообщений
message_history = []

# Добавьте дополнительные варианты ответов бота для каждого вопроса/фразы
# Обратите внимание, что ответы могут быть списками строк для разнообразия.

X_train = vectorizer.fit_transform([data[0] for data in train_data])
y_train = [random.choice(response_list) for _, response_list in train_data]
y_train = np.array(y_train)

classifier.fit(X_train, y_train)

photo_pattern = re.compile(r'фото[\w]*|картин[\w]*|изобра[\w]*|фотограф[\w]*', re.IGNORECASE)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Сохраняем сообщения в историю
    message_history.append(message.content)

    await image_on_message(message, bot, vectorizer, classifier, photo_pattern)

@bot.command()
async def history(ctx):
    """Отправляет историю сообщений."""
    history_str = '\n'.join(message_history[-10:])
    await ctx.send(f"История сообщений:\n{history_str}")

@bot.command()
async def menu(ctx):
    """Отправляет список доступных команд."""
    commands_list = [
        "!menu - Показать список команд",
        "!history - Отправить историю сообщений",
        "!weather [город] - Получить текущую погоду для указанного города",
        # Другие команды...
    ]

    # Подготовка списка команд с форматированием
    formatted_commands = "\n".join(commands_list)

    # Создание встраиваемого сообщения с заголовком, описанием и списком команд
    embed = discord.Embed(
        title="Меню команд",
        description="Пожалуйста, вот список доступных команд:",
        color=discord.Color.gold()  # Устанавливаем золотой цвет
    )
    embed.set_author(
        name=ctx.bot.user.name,
        icon_url=ctx.bot.user.avatar.url,
        url="https://www.example.com"  # Добавляем URL-адрес, по которому можно получить дополнительную информацию о боте
    )
    embed.add_field(
        name="Команды:", 
        value=formatted_commands, 
        inline=False
    )
    embed.set_footer(
        text="Для получения помощи по команде используйте: !help [команда]",
        icon_url=ctx.bot.user.avatar.url  # Иконка бота в подвале сообщения
    )
    embed.set_thumbnail(
        url="https://i.imgur.com/kBLi4Ke.png"  # Добавляем изображение в заголовок
    )
    embed.set_image(
        url="https://i.imgur.com/XYz66z3.png"  # Добавляем большое изображение в сообщение
    )

    # Отправка встраиваемого сообщения
    await ctx.send(embed=embed)

@bot.command()
async def weather(ctx, *, city: str):
    """Отправляет текущую погоду для указанного города."""
    weather_info = await get_weather(city)
    await ctx.send(weather_info)

# Дополнительные команды...
# Например, команда для получения случайного факта или шутки...

bot.run(config.token)
