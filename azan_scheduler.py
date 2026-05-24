import os
import requests
import time
from datetime import datetime, date
import pytz

local_tz = pytz.timezone("Europe/London")

def get_luton_times(for_date=None):
    """
    Fetch prayer times from Aladhan for Luton, UK.

    method=1  : University of Islamic Sciences, Karachi
    school=1  : Hanafi (later Asr) - matches Islamic Relief Luton timetable
    latitudeAdjustmentMethod=3 : One-Seventh of the Night (standard UK)
    """
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

def trigger_alexa():
    webhook_url = os.environ.get("VIRTUAL_DOORBELL_URL")
    if not webhook_url:
        print("[WARN] VIRTUAL_DOORBELL_URL secret is not set.")
        return
    try:
        resp = requests.get(webhook_url, timeout=10)
        print(f"[INFO] Alexa webhook triggered. Status: {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] Failed to trigger Alexa webhook: {e}")

def run():
    # When manually dispatched from GitHub Actions UI, fire immediately and exit.
    if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        print("[INFO] Manual dispatch detected — triggering Alexa now.")
        trigger_alexa()
        return

    prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    triggered_today = set()

    # Fetch today's times on startup
    today = date.today()
    timings = get_luton_times(today)
    if timings:
        print(f"[INFO] Prayer times loaded for {today}: " +
              ", ".join(f"{p}={timings[p]}" for p in prayers))
    else:
        print("[ERROR] Could not load initial prayer times. Will retry.")

    while True:
        now_local = datetime.now(local_tz)
        current_date = now_local.date()

        # At the start of each new day, refresh times and clear trigger log
        if current_date != today:
            today = current_date
            triggered_today.clear()
            timings = get_luton_times(today)
            if timings:
                print(f"[INFO] New day — prayer times refreshed for {today}: " +
                      ", ".join(f"{p}={timings[p]}" for p in prayers))
            else:
                print("[ERROR] Could not refresh prayer times for new day.")

        if timings:
            # Strip seconds from the API response times (they come as "HH:MM")
            # and compare to local wall-clock time (also "HH:MM").
            current_time_str = now_local.strftime("%H:%M")

            for prayer in prayers:
                prayer_time = timings[prayer][:5]  # Ensure "HH:MM" only
                if (current_time_str == prayer_time and
                        prayer not in triggered_today):
                    print(f"[INFO] {prayer} time reached ({prayer_time}). Triggering Alexa.")
                    trigger_alexa()
                    triggered_today.add(prayer)
                    # Sleep 61 seconds so we don't double-fire within the same minute
                    time.sleep(61)
                    break

        time.sleep(30)

if __name__ == "__main__":
    run()
