import os
import time
import datetime
import requests

# --- LUTON CONFIGURATION ---
CITY = "Luton"
COUNTRY = "UK"
METHOD = 3 # 3 = Muslim World League calculation method

VIRTUAL_DOORBELL_URL = os.environ.get("VIRTUAL_DOORBELL_URL")

def get_prayer_timings():
    url = f"https://api.aladhan.com/v1/timingsByCity?city={CITY}&country={COUNTRY}&method={METHOD}"
    try:
        response = requests.get(url).json()
        timings = response['data']['timings']
        return {
            'Fajr': timings['Fajr'],
            'Asr': timings['Asr'],
            'Maghrib': timings['Maghrib'],
            'Isha': timings['Isha']
        }
    except Exception as e:
        print(f"Error fetching times: {e}")
        return None

def main():
    print(f"Fetching prayer times for {CITY}...")
    prayers = get_prayer_timings()
    if not prayers: return

    print("Today's Targets (Luton Local Time):", prayers)

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        
        if current_time in prayers.values():
            prayer_name = [k for k, v in prayers.items() if v == current_time][0]
            print(f"Time for {prayer_name}! Ringing Alexa...")
            requests.get(VIRTUAL_DOORBELL_URL)
            time.sleep(65) # Avoid double triggering
            
        time.sleep(30)

if __name__ == "__main__":
    main()
