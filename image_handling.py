import discord
import requests
from io import BytesIO
from PIL import Image
import re
import random

image_urls = {
    'тянки': [
        'https://sun9-39.userapi.com/impg/GeJgPYGYxOtSQoDfzQHqq_pLkVW2hoCrBwodBw/RwmCez5ppOE.jpg?size=1125x1288&quality=96&sign=c20c4476638671f8939b695927c7375f&type=album',
    ],
    'машины': [
        'https://sun9-17.userapi.com/impg/k5CXaNeQvXELGFFV2U123qoDbMUolipTu87vIQ/pVbxASQBkaI.jpg?size=1000x720&quality=95&sign=3752a91ff2ea614d5d3e1b3038614cc4&type=album',
    ],
    'аниме': [
        'https://sun9-54.userapi.com/impg/_dMVodzAmqvDd9Plhb3m-hmvbaYFaQN3hHCO2Q/6BUW78WWT80.jpg?size=720x908&quality=95&sign=d0b3802f3eac727829da103a750e905b&type=album',
    ],
    'дединсульт': [
        'https://sun9-28.userapi.com/impg/OOrK6Sh5DlLxxAVDo1inWhuPgDRlvosDqzqS1w/6I-vPjkYTr8.jpg?size=736x707&quality=95&sign=258a0e972347456da3f95d5d795901ba&type=album',
    ],
    'мемасы': [
        'https://sun9-48.userapi.com/impg/BBixb5kM4KHZcRxoVb6d5wk8wstwcPYxSYCGjA/GfaZY76omRI.jpg?size=1200x840&quality=95&sign=0ed72c8128c7a3cccabfe6c0d485d3d2&type=album',
    ],
    'арты': [
        'https://sun9-38.userapi.com/impg/IHdGhPq60dY6FLIgiDQ9EMDhQVVz11gPrCGlUA/Nd4Lx98iDuk.jpg?size=2560x1435&quality=96&sign=17115793562cac225f83ad6028e8e9d3&type=album',
    ]
}

async def send_image(message, photo_url):
    response = requests.get(photo_url)
        
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        
        with BytesIO() as image_binary:
            image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))
    else:
        await message.channel.send("Не удалось загрузить изображение")

async def on_message(message, bot, vectorizer, classifier, photo_pattern):
    if message.author == bot.user:
        return

    # Если сообщение начинается с префикса команды, обрабатываем его как команду
    if message.content.startswith('!'):
        return

    input_vector = vectorizer.transform([message.content])
    predicted_response = classifier.predict(input_vector)

    # Проверяем, содержит ли сообщение ключевые слова для специфических ответов
    if "погода" in message.content.lower():
        # Если содержит ключевое слово "погода", отправляем информацию о погоде
        await message.channel.send("Дайте мне ваш город, и я проверю погоду для вас.")
    elif "анекдот" in message.content.lower():
        # Если содержит ключевое слово "анекдот", отправляем случайный анекдот
        await message.channel.send("Зачем программисту анекдоты? Чтобы улучшить свой юморной интерфейс!")
    elif "тянки" in message.content.lower():
        # Если содержит ключевое слово "анекдот", отправляем случайный анекдот
        await message.channel.send("Ща накалдую")
    elif "машины" in message.content.lower():
        # Если содержит ключевое слово "анекдот", отправляем случайный анекдот
        await message.channel.send("В пути к вам...")
    elif "аниме" in message.content.lower():
        # Если содержит ключевое слово "анекдот", отправляем случайный анекдот
        await message.channel.send("Рисуем...")
    elif "арты" in message.content.lower():
        # Если содержит ключевое слово "анекдот", отправляем случайный анекдот
        await message.channel.send("Пересматриваем ArtStation...")
    elif "мемасы" in message.content.lower():
        # Если содержит ключевое слово "анекдот", отправляем случайный анекдот
        await message.channel.send("Шерстим 4chan...")
    elif "дединсульт" in message.content.lower():
        # Если содержит ключевое слово "анекдот", отправляем случайный анекдот
        await message.channel.send("Чел живи...")
    elif "меню" in message.content.lower():  # Добавляем проверку на слово "меню"
        await menu(message.channel)  # Вызываем функцию отображения меню
    else:
        # Во всех остальных случаях отправляем предсказанный ответ
        await message.channel.send(predicted_response[0])

    if photo_pattern.search(message.content):
        await message.channel.send("Выберите категорию изображений: Выберите из: тянки, машины, аниме, дединсульт, мемасы, арты")

     # Обработка запросов на изображения...
    for category, urls in image_urls.items():
        if category.lower() in message.content.lower():
            photo_url = random.choice(urls)
            await send_image(message, photo_url)

    # Обработка запросов на изображения...
    # Проверяем, содержит ли сообщение ключевое слово "природа" и отправляем фотографии природы
    if 'тянки' in message.content.lower():
        photo_urls = image_urls.get('тянки')
        if photo_urls:
            photo_url = random.choice(photo_urls)
            await send_image(message, photo_url)

    # Проверяем, содержит ли сообщение ключевое слово "машины" и отправляем фотографии машин
    if 'машины' in message.content.lower():
        photo_urls = image_urls.get('машины')
        if photo_urls:
            photo_url = random.choice(photo_urls)
            await send_image(message, photo_url)

    # Проверяем, содержит ли сообщение ключевое слово "аниме" и отправляем фотографии аниме
    if 'аниме' in message.content.lower():
        photo_urls = image_urls.get('аниме')
        if photo_urls:
            photo_url = random.choice(photo_urls)
            await send_image(message, photo_url)

    # Проверяем, содержит ли сообщение ключевое слово "аниме" и отправляем фотографии аниме
    if 'дединсульт' in message.content.lower():
        photo_urls = image_urls.get('дединсульт')
        if photo_urls:
            photo_url = random.choice(photo_urls)
            await send_image(message, photo_url)

    # Проверяем, содержит ли сообщение ключевое слово "аниме" и отправляем фотографии аниме
    if 'мемасы' in message.content.lower():
        photo_urls = image_urls.get('мемасы')
        if photo_urls:
            photo_url = random.choice(photo_urls)
            await send_image(message, photo_url)

    # Проверяем, содержит ли сообщение ключевое слово "аниме" и отправляем фотографии аниме
    if 'арты' in message.content.lower():
        photo_urls = image_urls.get('арты')
        if photo_urls:
            photo_url = random.choice(photo_urls)
            await send_image(message, photo_url)
        
    # Обработка запросов на команды...
    await bot.process_commands(message)
