import os

from pyowm.owm import OWM
from pyowm.weatherapi25.weather import Weather

owm = OWM(os.environ.get('owm_token'))
weather_mgr = owm.weather_manager()


def get_forecast():
    three_h_forecast = weather_mgr.forecast_at_place('Moscow,RU', '3h').forecast
    print(three_h_forecast)
    for weather in three_h_forecast:
        show_weather(weather)
        print('---------------')


def get_current_weather():
    observation = weather_mgr.weather_at_place('Krasnoarmeysk,RU')
    weather: Weather = observation.weather
    show_weather(weather)


def get_forecast_coords():
    three_h_forecast = weather_mgr.forecast_at_coords(lat=56.129304, lon=38.12551, interval='3h').forecast
    print(three_h_forecast)
    for weather in three_h_forecast:
        show_weather(weather)
        print('---------------')


def get_current_weather_coords(lat, lon):
    observation = weather_mgr.weather_at_coords(lat=lat, lon=lon)
    weather: Weather = observation.weather
    show_weather(weather)


def show_weather(weather: Weather):
    print(f'Время: {weather.reference_time("iso")}')
    print(f'Погода: {weather.status}')
    print(f'Погода (детально): {weather.detailed_status}')
    print(f'Температура: {weather.temp}')
    print(f'Температура (Цельсии): {weather.temperature("celsius")}')


def main():
    get_current_weather()
    get_current_weather_coords(lat=56.129304, lon=38.12551)
    # get_forecast()


if __name__ == '__main__':
    main()
