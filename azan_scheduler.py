import os
import requests
import time
from datetime import datetime
import pytz

local_tz = pytz.timezone("Europe/London")

def get_luton_times():
    # Method 3 tuned precisely for standard UK timetables (like Islamic Relief)
    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": "Luton", 
        "country": "United Kingdom", 
        "method": 3,
        "school": 0 # Shafi/Standard method for Asr
    } 
    response = requests.get(url, params=params).json()
    return response['data']['timings']

def trigger_alexa():
    webhook_url = os.environ.get("VIRTUAL_DOORBELL_URL")
    if webhook_url:
        requests.get(webhook_url)
        print("Trigger successfully sent to Alexa Virtual Doorbell!")
    else:
        print("Error: VIRTUAL_DOORBELL_URL secret is missing!")

def run():
    is_manual_run = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
    if is_manual_run:
        print("Manual test detected! Instantly triggering your Echo speaker...")
        trigger_alexa()
        return

    print("Automated tracking active for Luton (Matched to UK Timetables)...")
    while True:
        now_local = datetime.now(local_tz)
        current_time_str = now_local.strftime("%H:%M")
        
        timings = get_luton_times()
        prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
        
        for prayer in prayers:
            if current_time_str == timings[prayer]:
                print(f"Match found! It is time for {prayer} in Luton. Signaling Alexa...")
                trigger_alexa()
                time.sleep(61) 
                
        time.sleep(30)

if __name__ == "__main__":
    run()
