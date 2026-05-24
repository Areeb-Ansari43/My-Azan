import os
import requests
import time
from datetime import datetime, date
import pytz

local_tz = pytz.timezone("Europe/London")

def get_luton_times(for_date=None):
    if for_date is None:
        for_date = date.today()
    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": "Luton",
        "country": "United Kingdom",
        "method": 1,
        "school": 1,
        "latitudeAdjustmentMethod": 3,
        "date": for_date.strftime("%d-%m-%Y"),
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["data"]["timings"]
    except Exception as e:
        print(f"[ERROR] Could not fetch prayer times: {e}")
        return None

def trigger_alexa(prayer_name, prayer_time):
    webhook_url = os.environ.get("VIRTUAL_DOORBELL_URL")
    if not webhook_url:
        print("[WARN] VIRTUAL_DOORBELL_URL secret is not set.")
        return
    try:
        # Pass prayer name and time as URL parameters
        # e.g. https://yourwebhook.com?prayer=Maghrib&time=20:53
        separator = "&" if "?" in webhook_url else "?"
        full_url = f"{webhook_url}{separator}prayer={prayer_name}&ptime={prayer_time}"
        resp = requests.get(full_url, timeout=10)
        print(f"[INFO] Triggered Alexa for {prayer_name} at {prayer_time}. Status: {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] Failed to trigger Alexa webhook: {e}")

def run():
    if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        print("[INFO] Manual dispatch — triggering Alexa now for testing.")
        # For manual test, fetch current prayer
        timings = get_luton_times()
        if timings:
            now = datetime.now(local_tz)
            hour = now.hour
            prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
            if hour >= 2 and hour < 12:
                prayer = "Fajr"
            elif hour >= 12 and hour < 16:
                prayer = "Dhuhr"
            elif hour >= 16 and hour < 19:
                prayer = "Asr"
            elif hour >= 19 and hour < 22:
                prayer = "Maghrib"
            else:
                prayer = "Isha"
            prayer_time = timings[prayer][:5]
            trigger_alexa(prayer, prayer_time)
        return

    prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    triggered_today = set()
    today = date.today()
    timings = get_luton_times(today)

    if timings:
        print(f"[INFO] Prayer times for {today}: " +
              ", ".join(f"{p}={timings[p][:5]}" for p in prayers))

    while True:
        now_local = datetime.now(local_tz)
        current_date = now_local.date()

        if current_date != today:
            today = current_date
            triggered_today.clear()
            timings = get_luton_times(today)
            if timings:
                print(f"[INFO] Refreshed times for {today}: " +
                      ", ".join(f"{p}={timings[p][:5]}" for p in prayers))

        if timings:
            current_time_str = now_local.strftime("%H:%M")
            for prayer in prayers:
                prayer_time = timings[prayer][:5]
                if current_time_str == prayer_time and prayer not in triggered_today:
                    print(f"[INFO] {prayer} at {prayer_time} — triggering Alexa.")
                    trigger_alexa(prayer, prayer_time)
                    triggered_today.add(prayer)
                    time.sleep(61)
                    break

        time.sleep(30)

if __name__ == "__main__":
    run()
