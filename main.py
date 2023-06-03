import datetime as dt
import requests
import click
import keyboard
import time
import sys

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "caeeedf4d555caa772563d80ee0bde04"

def set_city():
    global CITY
    CITY = input("Enter city name: ")

set_city()

URL =  BASE_URL + "q=" + CITY + "&appid=" + API_KEY

global response 
response = requests.get(URL).json()
if(response["cod"] == "404" or CITY == ""):
    click.echo("Enter correct details")
    sys.exit()
options = ["Coordinates", "Weather", "Visibility", "Wind", "Clouds", "Sunrise/Sunset","Feels like","Exit"]

@click.command()
def get_coordiantes():
    lon,lat = response['coord']['lon'],response['coord']['lat']
    click.echo("Coordinates->")
    click.echo("Longitude -> " + str(lon) +"°")
    click.echo("Latitude -> " + str(lat)+"°")
    pass

@click.command()
def get_weather():
    temp_k = response["main"]["temp"]
    temp_c, temp_f = to_celsius(temp_k)
    click.echo(f"Temperature -> {temp_c:.2f}C || {temp_f:.2f}F")

@click.command()
def get_visibility():
    visibility = response["visibility"]
    click.echo(f"Visibility -> {visibility} meters")

@click.command()
def get_wind():
    wind_speed = response["wind"]["speed"]
    wind_deg = response["wind"]["deg"]
    click.echo(f"Wind speed -> {wind_speed} m/s\nWind degree -> {wind_deg}°")

@click.command()
def get_clouds():
    clouds = response["clouds"]["all"]
    click.echo(f"Clouds -> {clouds} %")

@click.command()
def get_sunrise_sunset():
    sunrise_time = dt.datetime.utcfromtimestamp(response["sys"]["sunrise"] + response["timezone"])
    sunset_time = dt.datetime.utcfromtimestamp(response["sys"]["sunset"] + response["timezone"])
    click.echo(f"Sunrise -> {sunrise_time.strftime('%H:%M:%S')}\nSunset -> {sunset_time.strftime('%H:%M:%S')}")

@click.command()
def feels_like():
    feels_like_k = response["main"]["feels_like"]
    feels_like_c, feels_like_f = to_celsius(feels_like_k)
    temp_max_k = response["main"]["temp_max"]
    temp_max_c, temp_max_f = to_celsius(temp_max_k)
    temp_min_k = response["main"]["temp_min"]
    temp_min_c, temp_min_f = to_celsius(temp_min_k)
    click.echo(f"Feels like -> {feels_like_c:.2f}C || {feels_like_f:.2f}F\nMax temperature -> {temp_max_c:.2f}C || {temp_max_f:.2f}F\nMin temperature -> {temp_min_c:.2f}C || {temp_min_f:.2f}F")

@click.command()
def exit():
    click.echo("Exit")
    sys.exit()

def select_previous_option():
    global selected_option
    selected_option = (selected_option - 1) % len(options)

def select_next_option():
    global selected_option
    selected_option = (selected_option + 1) % len(options)

def handle_selection():
    click.clear()
    click.echo(f"You selected: {options[selected_option]}")

    # Perform action based on selection
    if selected_option == 0:
        get_coordiantes()
    elif selected_option == 1:
        get_weather()
    elif selected_option == 2:
        get_visibility()
    elif selected_option == 3:
        get_wind()
    elif selected_option == 4:
        get_clouds()
    elif selected_option == 5:
        get_sunrise_sunset()
    elif selected_option == 6:
        feels_like()
    elif selected_option == 7:
        exit()


def display_menu():
    click.clear()
    click.echo("Weather App")
    click.echo("============")
    click.echo("Select an option:")
    for i, option in enumerate(options):
        click.echo(f"[{'x' if i == selected_option else ' '}] {option}")

    while True:
        if keyboard.is_pressed('up'):
            select_previous_option()
            display_menu()
            break
        elif keyboard.is_pressed('down'):
            select_next_option()
            display_menu()
            break
        elif keyboard.is_pressed('enter'):
            handle_selection()
            break
        time.sleep(0.1)


def to_celsius(kelvin):
    deg_c = kelvin - 273.15
    deg_f = deg_c * 9/5 + 32
    return deg_c, deg_f


def main():
    global selected_option
    selected_option = 0
    display_menu()


if __name__ == "__main__":
    main()