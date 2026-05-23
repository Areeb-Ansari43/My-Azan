import os
import requests
import time
from datetime import datetime
import pytz

# Target timezone for Luton
local_tz = pytz.timezone("Europe/London")

def get_luton_times():
    # Fetching exact astronomical prayer times for Luton (Method 3 = Muslim World League / UK standard)
    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {"city": "Luton", "country": "United Kingdom", "method": 3} 
    response = requests.get(url, params=params).json()
    return response['data']['timings']

def trigger_alexa():
    webhook_url = os.environ.get("VIRTUAL_DOORBELL_URL")
    if webhook_url:
        requests.get(webhook_url)
        print("Trigger successfully sent to Virtual Smart Home!")
    else:
        print("Error: VIRTUAL_DOORBELL_URL secret is missing!")

def run():
    # Detect if you pressed the manual test button on GitHub
    is_manual_run = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
    if is_manual_run:
        print("Manual test detected! Instantly triggering your Echo speaker...")
        trigger_alexa()
        return

    print("Automated tracking started for Luton (BST-aware)...")
    while True:
        # Get exact current time in Luton
        now_local = datetime.now(local_tz)
        current_time_str = now_local.strftime("%H:%M")
        
        timings = get_luton_times()
        prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
        
        for prayer in prayers:
            # Check if current local time matches the local prayer time
            if current_time_str == timings[prayer]:
                print(f"Match found! It is time for {prayer} in Luton. Signaling Alexa...")
                trigger_alexa()
                time.sleep(61) # Prevent double triggering
                
        time.sleep(30)

if __name__ == "__main__":
    run()
