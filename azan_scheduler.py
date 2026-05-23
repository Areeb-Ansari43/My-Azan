import os
import requests
import time
from datetime import datetime, timedelta
import pytz

local_tz = pytz.timezone("Europe/London")

def get_luton_times():
    # Method 3 is the standard UK calculation method
    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {"city": "Luton", "country": "United Kingdom", "method": 3} 
    response = requests.get(url, params=params).json()
    raw_timings = response['data']['timings']
    
    # Core prayers to track
    prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    corrected_timings = {}
    
    # Shift times by 1 hour back to line up the cloud servers with local UK clocks perfectly
    for prayer in prayers:
        time_obj = datetime.strptime(raw_timings[prayer], "%H:%M")
        corrected_time = (time_obj - timedelta(hours=1)).strftime("%H:%M")
        corrected_timings[prayer] = corrected_time
        
    return corrected_timings

def trigger_alexa():
    webhook_url = os.environ.get("VIRTUAL_DOORBELL_URL")
    if webhook_url:
        requests.get(webhook_url)
        print("Trigger successfully sent to Alexa!")
    else:
        print("Error: VIRTUAL_DOORBELL_URL secret is missing!")

def run():
    is_manual_run = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
    if is_manual_run:
        print("Manual test detected! Triggering speaker instantly...")
        trigger_alexa()
        return

    print("Automated tracking started for Luton (Time-corrected)...")
    while True:
        # Get current time in London/Luton
        now_local = datetime.now(local_tz)
        current_time_str = now_local.strftime("%H:%M")
        
        timings = get_luton_times()
        
        for prayer, p_time in timings.items():
            if current_time_str == p_time:
                print(f"Match found! It is time for {prayer} in Luton. Signaling Alexa...")
                trigger_alexa()
                time.sleep(61) 
                
        time.sleep(30)

if __name__ == "__main__":
    run()
    run()
