import os
import requests
import time
from datetime import datetime, date
import pytz

local_tz = pytz.timezone("Europe/London")

# Manual offsets in minutes to match Islamic Relief Luton timetable exactly.
# Based on today's comparison:
#   API returns Isha 22:04, IR Luton says 22:13 → +9 minutes
#   Check each prayer tomorrow and report any differences.
OFFSETS = {
    "Fajr":    0,
    "Dhuhr":   0,
    "Asr":     0,
    "Maghrib": 0,
    "Isha":    9,
}

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
        timings = data["data"]["timings"]

        # Apply offsets to match Islamic Relief Luton timetable
        adjusted = {}
        for prayer, offset in OFFSETS.items():
            raw = timings[prayer][:5]
            if offset != 0:
                h, m = map(int, raw.split(":"))
                total = h * 60 + m + offset
                total = total % (24 * 60)
                adjusted[prayer] = f"{total // 60:02d}:{total % 60:02d}"
            else:
                adjusted[prayer] = raw

        return adjusted
    except Exception as e:
        print(f"[ERROR] Could not fetch prayer times: {e}")
        return None

def trigger_alexa(prayer_name, prayer_time):
    webhook_url = os.environ.get("VIRTUAL_DOORBELL_URL")
    if not webhook_url:
        print("[WARN] VIRTUAL_DOORBELL_URL secret is not set.")
        return
    try:
        separator = "&" if "?" in webhook_url else "?"
        full_url = f"{webhook_url}{separator}prayer={prayer_name}&ptime={prayer_time}"
        resp = requests.get(full_url, timeout=10)
        print(f"[INFO] Triggered {prayer_name} at {prayer_time}. Status: {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] Failed to trigger Alexa: {e}")

def run():
    if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        print("[INFO] Manual dispatch — triggering now for testing.")
        timings = get_luton_times()
        if timings:
            now = datetime.now(local_tz)
            hour = now.hour
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
            trigger_alexa(prayer, timings[prayer])
        return

    prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    triggered_today = set()
    today = date.today()
    timings = get_luton_times(today)

    if timings:
        print(f"[INFO] Adjusted times for {today}: " +
              ", ".join(f"{p}={timings[p]}" for p in prayers))

    while True:
        now_local = datetime.now(local_tz)
        current_date = now_local.date()

        if current_date != today:
            today = current_date
            triggered_today.clear()
            timings = get_luton_times(today)
            if timings:
                print(f"[INFO] New day times: " +
                      ", ".join(f"{p}={timings[p]}" for p in prayers))

        if timings:
            current_time_str = now_local.strftime("%H:%M")
            for prayer in prayers:
                if current_time_str == timings[prayer] and prayer not in triggered_today:
                    print(f"[INFO] {prayer} at {timings[prayer]} — triggering.")
                    trigger_alexa(prayer, timings[prayer])
                    triggered_today.add(prayer)
                    time.sleep(61)
                    break

        time.sleep(30)

if __name__ == "__main__":
    run()
