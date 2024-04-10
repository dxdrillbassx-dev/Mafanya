import requests
import config

async def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={config.weather_api_key}&q={city}&units=metric&lang=ru"
    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        main = weather_data["main"]
        temperature = main["temp"]
        humidity = main["humidity"]
        pressure = main["pressure"]
        weather = weather_data["weather"]
        weather_description = weather[0]["description"]
        return f"В городе {city} сейчас {weather_description}, температура {temperature}°C, влажность {humidity}%, давление {pressure} гПа."
    else:
        return "Город не найден, попробуйте еще раз."
