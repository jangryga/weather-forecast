import sys
from weather_wizzard.WeatherWizzard import WeatherWizzard


def main(args):
    if len(args) != 1:
        sys.stderr.write("Usage: change_name.py <id>\n")
        sys.exit(1)

    id = args[0]

    user_input = input(f"Where to save the answers? [Enter to save in current directory] ")

    weather_wizzard = WeatherWizzard(id, user_input) if user_input else WeatherWizzard(id)

    data = [
        {
            "question_one": weather_wizzard.get_weather_in_city("bath", "wednesday", 10),
            "question_two": weather_wizzard.is_pressure_below_value("edinburgh", 1000, "friday"),
            "question_three": weather_wizzard.get_median_temp_in_city("cardiff"),
            "question_four": weather_wizzard.find_city_with_highest_wind_speed(),
            "question_five": weather_wizzard.will_it_snow(),
        }
    ]

    weather_wizzard.save_json_data(data)


if __name__ == "__main__":
    main(sys.argv[1:])
