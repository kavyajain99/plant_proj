import requests
import datetime
import random 
from twilio.rest import Client

# Weather API
# weather_api_key = "ba77a69e7846e1208114b72b0b66139f"
# weather_url = "http://api.openweathermap.org/data/2.5/weather?q=Cypress,US&appid=" + weather_api_key + "&units=imperial" 

# attempt 2 of weather API connect 

lat = 29.9719  # Latitude of Cypress, TX
lon = -95.6911 # Longitude of Cypress, TX
weather_api_key = "ba77a69e7846e1208114b72b0b66139f"
weather_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_api_key}&units=imperial"

# Twilio
twilio_account_sid = "ACb91c70fc6a3394bc122a7e5bcb33e508"
twilio_auth_token = "a67d456b00632cb6c644104678865abf"
twilio_phone_number = "+18555967198"
your_phone_number = "+18603316206"

#this function returns a random string to be sent. it takes in the low temp
def coldMessage(low):
    randomInt = random.randint(0,19)
    
    if randomInt == 0:
        return f"Make sure to bundle up, little plant pals—it's about to get chilly! The midnight low will be {low}°F."
    elif randomInt == 1:
        return f"Don’t let your plants freeze, unless you’re trying to start an ice garden. The midnight low will be {low}°F."
    elif randomInt == 2:
        return f"Time to save your plants from becoming frozen statues. The midnight low will be {low}°F."
    elif randomInt == 3:
        return f"It’s cold enough outside to give your plants frostbite. Better bring them in! The midnight low will be {low}°F."
    elif randomInt == 4:
        return f"Reminder: Plants don’t like winter sports. Get them inside before they turn into popsicles. The midnight low will be {low}°F."
    elif randomInt == 5:
        return f"If you love your plants, now would be a good time to rescue them from the cold. The midnight low will be {low}°F."
    elif randomInt == 6:
        return f"Your plants are getting cold out there—they’re not built for the arctic! The midnight low will be {low}°F."
    elif randomInt == 7:
        return f"Your plants are about to enter hibernation mode—unless they come inside, of course. The midnight low will be {low}°F."
    elif randomInt == 8:
        return f"The plants are giving you the silent treatment out there. Maybe they’re cold? The midnight low will be {low}°F."
    elif randomInt == 9:
        return f"Just a heads up—your plants are about to get a frosty makeover. Rescue mission, anyone? The midnight low will be {low}°F."
    elif randomInt == 10:
        return f"If you don’t bring them in, they might decide they want to be snowmen instead of houseplants. The midnight low will be {low}°F."
    elif randomInt == 11:
        return f"The weather’s so cold, your plants will be asking for a blanket if they stay outside. The midnight low will be {low}°F."
    elif randomInt == 12:
        return f"Don’t let your plants become winter casualties. Time to get them indoors! The midnight low will be {low}°F."
    elif randomInt == 13:
        return f"Time to prevent a plant popsicle situation. Inside they go! The midnight low will be {low}°F."
    elif randomInt == 14:
        return f"If you want to keep your plants alive and not frozen, inside is the place to be. The midnight low will be {low}°F."
    elif randomInt == 15:
        return f"It’s so cold, even your plants are thinking of taking a vacation inside. The midnight low will be {low}°F."
    elif randomInt == 16:
        return f"Cold weather is creeping in. Your plants need a warm refuge, stat! The midnight low will be {low}°F."
    elif randomInt == 17:
        return f"The plants are currently experiencing sub-zero temperatures. A little shelter, please! The midnight low will be {low}°F."
    elif randomInt == 18:
        return f"If you don't want your plants turning into sad little frozen things, bring them inside. The midnight low will be {low}°F."
    elif randomInt == 19:
        return f"Your plants are not in the mood for an ice age. Time to bring them in and save them from the cold. The midnight low will be {low}°F."
    else: 
        return "meow you've made an error, Kavya"


try:
    response = requests.get(weather_url) 
    response.raise_for_status() #If the status code indicates an error ... 404 Not Found... raises an HTTPError exception.
    forecast_data = response.json() #converts it into a Python dictionary or list

    message_body = ""

    # Find tomorrow's 3 AM low temperature
    tomorrow_3am_low = None #none means null in python
    tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)  # Tomorrow's date

    for forecast in forecast_data["list"]:
        forecast_time_str = forecast["dt_txt"] #value is a string representing the date and time of the forecast
        forecast_datetime = datetime.datetime.strptime(forecast_time_str, "%Y-%m-%d %H:%M:%S")

        
        if forecast_datetime.date() == tomorrow_date and forecast_datetime.hour == 3:
            tomorrow_3am_low = forecast["main"]["temp_min"]
            break  # stop checking after finding tomorrow's 3 AM forecast
        
    # Just a test block    
    if tomorrow_3am_low is not None:
        print(tomorrow_3am_low)    

    if tomorrow_3am_low is not None and tomorrow_3am_low < 100:
        message_body = coldMessage(tomorrow_3am_low)
        print("Tomorrow 3 AM cold message selected.")

    if message_body: 
        client = Client(twilio_account_sid, twilio_auth_token) #makes a Client object from the Twilio library
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=your_phone_number,
        )
        print("SMS sent successfully!")
    else: #the message body is still none which means > cold temp 
        print("No conditions met for message sending.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching weather data: {e}")
except KeyError as e:
    print(f"Error parsing weather data: {e}")
except Exception as e:
    print(f"An error occurred: {e}")