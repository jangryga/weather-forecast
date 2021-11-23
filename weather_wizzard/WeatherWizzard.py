import os
from typing import List
import requests
import json


class WeatherWizzard:

    _default_path = os.path.dirname(os.path.abspath(__file__))
    _url = "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/"

    def __init__(self, id: int, path: str = _default_path, url: str = _url):
        self.id = id
        self.path = path
        self.url = url

    def __str__(self) -> str:
        return f" Id: {self.id}\n Url: {self.url}\n Save path: {self.path}"

    def get_weather_in_city(self, city: str, day: str, time: int) -> int:
        """Get temperature in city at a specified day and time

        Args:
            city (str): Lowercase city name
            day (str): Lowercase day name
            time (int): Hour of measurement in range 1 to 24

        Returns:
            int: Temperature
        """
        weather_in_city = requests.get(f"{self.url}/{self.id}/{city}").json()
        temp_day_hour = weather_in_city[f"{day}"][time]["temperature"]
        return temp_day_hour

    def is_pressure_below_value(self, city: str, value: int, day: str) -> bool:
        """Will the pressure go below a specified value

        Args:
            city (str): City for the measurement
            value (int): Pressure value
            day (str): Day of the week

        Returns:
            bool: True or False
        """
        weather_on_day = requests.get(f"{self.url}/{self.id}/{city}").json()[day]
        pressure = [item["pressure"] < value for item in weather_on_day]
        return pressure == []

    def get_median_temp_in_city(self, city: str) -> int:
        """Get all temperatures in a city for the week.
        Sort the array and return median value.

        Args:
            city (str): Name of the city

        Returns:
            int: Median temperature
        """
        weather_in_city = requests.get(f"{self.url}/{self.id}/{city}").json()
        temps_in_city = []
        for day in weather_in_city.values():
            for timeframe in day:
                temps_in_city.append(timeframe["temperature"])
        temps_in_city.sort()

        return int((temps_in_city[84] + temps_in_city[85]) / 2)

    def find_city_with_highest_wind_speed(self) -> str:
        """Get current list of cities.
        Get max wind speed for each of the cities and return the name of the city where the speed is recorded.
        If more then one city has the same highest speed, return first one in alphabetical order

        Returns:
            str: City with the highest wind speed next week
        """
        cities = requests.get("http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/cities/").json()[
            "cities"
        ]
        cities_speed = {city: self.get_max_wind_speed(city) for city in cities}
        max_wind_speed = max(cities_speed.values())
        cities_max_speed = [name for name, value in cities_speed.items() if value == max_wind_speed]
        return sorted(cities_max_speed)[0]

    def get_max_wind_speed(self, city: str) -> int:
        """Helper function.
        Get max wind speed in a given city for next week

        Args:
            city (str): City name

        Returns:
            int: Highest wind speed value
        """
        weather_in_city = requests.get(f"{self.url}/{self.id}/{city}").json()
        max_wind_speed = -float("inf")
        for day in weather_in_city.values():
            for timeframe in day:
                if timeframe["wind_speed"] > max_wind_speed:
                    max_wind_speed = timeframe["wind_speed"]
        return max_wind_speed

    def will_it_snow(self) -> bool:
        """Get current list of cities.
        Check if it will snow in any of them

        Returns:
            bool: False if it won't snow in any of the cities. True otherwise.
        """
        cities = requests.get("http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/cities/").json()[
            "cities"
        ]

        for city in cities:
            if self.will_snow_in_city(city):
                return True

        return False

    def will_snow_in_city(self, city: str) -> bool:
        """Will it snow in current city.
        It will snow if percipitation is above 0 and temperature is < 2 degrees.

        Args:
            city (str): Name of the city

        Returns:
            bool: True of False
        """
        weather_in_city = requests.get(f"{self.url}/{self.id}/{city}").json()
        for day in weather_in_city.values():
            for timeframe in day:
                if timeframe["precipitation"] > 0 and timeframe["temperature"] < 2:
                    return True
        return False

    def save_json_data(self, data: List) -> None:
        """Save json data to specified location.

        Args:
            data (List): Data formated as list
        """
        with open(f"{self.path}/answers.json", "w") as f:
            json.dump(data, f)
