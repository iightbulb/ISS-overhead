import requests
from datetime import datetime
import smtplib
import time
import os
from dotenv import load_dotenv

MY_LAT = -33.924870
MY_LONG = 18.424055


def configure():
    load_dotenv()


def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_lat <= MY_LAT + 5 and MY_LONG - 5 <= iss_long <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    hour = time_now.hour
    if hour <= sunrise or hour >= sunset:
        return True


def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:  # URL OF EMAIL SERVER
        connection.starttls()
        connection.login(os.getenv('my_email'), os.getenv('my_password'))
        connection.sendmail(
            from_addr=os.getenv('my_email'),
            to_addrs=os.getenv('my_email'),
            msg="Subject: LOOK UP")
    print("email sent")


configure()

while True:
    time.sleep(60)
    if is_overhead() and is_night():
        send_email()
    else:
        print("email not sent")






