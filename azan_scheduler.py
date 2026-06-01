import os
import requests
import time
from datetime import datetime, date
import pytz

local_tz = pytz.timezone("Europe/London")

# =============================================================================
# PRAYER TIMETABLE — Luton Central Mosque
# Only Fajr Start, Zuhr Start, Asr Start, Maghrib, Isha Start
# Update this at the end of each month with the new timetable.
# =============================================================================
TIMETABLE = {
    # June 2026
    (2026, 6, 1):  {"Fajr": "02:55", "Dhuhr": "13:05", "Asr": "18:33", "Maghrib": "21:15", "Isha": "22:30"},
    (2026, 6, 2):  {"Fajr": "02:54", "Dhuhr": "13:05", "Asr": "18:33", "Maghrib": "21:16", "Isha": "22:31"},
    (2026, 6, 3):  {"Fajr": "02:53", "Dhuhr": "13:05", "Asr": "18:34", "Maghrib": "21:17", "Isha": "22:32"},
    (2026, 6, 4):  {"Fajr": "02:52", "Dhuhr": "13:05", "Asr": "18:34", "Maghrib": "21:18", "Isha": "22:33"},
    (2026, 6, 5):  {"Fajr": "02:51", "Dhuhr": "13:05", "Asr": "18:35", "Maghrib": "21:19", "Isha": "22:34"},
    (2026, 6, 6):  {"Fajr": "02:50", "Dhuhr": "13:06", "Asr": "18:35", "Maghrib": "21:20", "Isha": "22:35"},
    (2026, 6, 7):  {"Fajr": "02:49", "Dhuhr": "13:06", "Asr": "18:36", "Maghrib": "21:21", "Isha": "22:36"},
    (2026, 6, 8):  {"Fajr": "02:49", "Dhuhr": "13:06", "Asr": "18:36", "Maghrib": "21:22", "Isha": "22:37"},
    (2026, 6, 9):  {"Fajr": "02:48", "Dhuhr": "13:06", "Asr": "18:36", "Maghrib": "21:22", "Isha": "22:38"},
    (2026, 6, 10): {"Fajr": "02:47", "Dhuhr": "13:06", "Asr": "18:37", "Maghrib": "21:23", "Isha": "22:39"},
    (2026, 6, 11): {"Fajr": "02:47", "Dhuhr": "13:07", "Asr": "18:37", "Maghrib": "21:24", "Isha": "22:40"},
    (2026, 6, 12): {"Fajr": "02:46", "Dhuhr": "13:07", "Asr": "18:38", "Maghrib": "21:24", "Isha": "22:41"},
    (2026, 6, 13): {"Fajr": "02:46", "Dhuhr": "13:07", "Asr": "18:38", "Maghrib": "21:25", "Isha": "22:42"},
    (2026, 6, 14): {"Fajr": "02:45", "Dhuhr": "13:07", "Asr": "18:38", "Maghrib": "21:26", "Isha": "22:43"},
    (2026, 6, 15): {"Fajr": "02:45", "Dhuhr": "13:07", "Asr": "18:39", "Maghrib": "21:26", "Isha": "22:43"},
    (2026, 6, 16): {"Fajr": "02:45", "Dhuhr": "13:08", "Asr": "18:39", "Maghrib": "21:27", "Isha": "22:44"},
    (2026, 6, 17): {"Fajr": "02:45", "Dhuhr": "13:08", "Asr": "18:39", "Maghrib": "21:27", "Isha": "22:44"},
    (2026, 6, 18): {"Fajr": "02:45", "Dhuhr": "13:08", "Asr": "18:40", "Maghrib": "21:27", "Isha": "22:45"},
    (2026, 6, 19): {"Fajr": "02:45", "Dhuhr": "13:08", "Asr": "18:40", "Maghrib": "21:28", "Isha": "22:45"},
    (2026, 6, 20): {"Fajr": "02:45", "Dhuhr": "13:09", "Asr": "18:40", "Maghrib": "21:28", "Isha": "22:46"},
    (2026, 6, 21): {"Fajr": "02:45", "Dhuhr": "13:09", "Asr": "18:40", "Maghrib": "21:28", "Isha": "22:46"},
    (2026, 6, 22): {"Fajr": "02:45", "Dhuhr": "13:09", "Asr": "18:41", "Maghrib": "21:28", "Isha": "22:46"},
    (2026, 6, 23): {"Fajr": "02:46", "Dhuhr": "13:09", "Asr": "18:41", "Maghrib": "21:29", "Isha": "22:46"},
    (2026, 6, 24): {"Fajr": "02:46", "Dhuhr": "13:09", "Asr": "18:41", "Maghrib": "21:29", "Isha": "22:46"},
    (2026, 6, 25): {"Fajr": "02:47", "Dhuhr": "13:10", "Asr": "18:41", "Maghrib": "21:29", "Isha": "22:46"},
    (2026, 6, 26): {"Fajr": "02:47", "Dhuhr": "13:10", "Asr": "18:41", "Maghrib": "21:29", "Isha": "22:46"},
    (2026, 6, 27): {"Fajr": "02:48", "Dhuhr": "13:10", "Asr": "18:41", "Maghrib": "21:29", "Isha": "22:46"},
    (2026, 6, 28): {"Fajr": "02:49", "Dhuhr": "13:10", "Asr": "18:41", "Maghrib": "21:28", "Isha": "22:46"},
    (2026, 6, 29): {"Fajr": "02:49", "Dhuhr": "13:10", "Asr": "18:41", "Maghrib": "21:28", "Isha": "22:45"},
    (2026, 6, 30): {"Fajr": "02:50", "Dhuhr": "13:11", "Asr": "18:41", "Maghrib": "21:28", "Isha": "22:45"},
}

def get_todays_times():
    now = datetime.now(local_tz)
    key = (now.year, now.month, now.day)
    return TIMETABLE.get(key, None)

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

def trigger_end_of_month_reminder():
    webhook_url = os.environ.get("VIRTUAL_DOORBELL_URL")
    if not webhook_url:
        return
    try:
        separator = "&" if "?" in webhook_url else "?"
        full_url = f"{webhook_url}{separator}prayer=reminder&ptime=00:00"
        resp = requests.get(full_url, timeout=10)
        print(f"[INFO] End of month reminder triggered. Status: {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] Failed to trigger reminder: {e}")

def run():
    now = datetime.now(local_tz)

    # Check if it's the last day of the month — trigger reminder
    tomorrow = date(now.year, now.month, now.day)
    import calendar
    last_day = calendar.monthrange(now.year, now.month)[1]
    if now.day == last_day:
        print("[INFO] Last day of month — triggering timetable reminder.")
        trigger_end_of_month_reminder()
        return

    if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        print("[INFO] Manual dispatch — triggering now for testing.")
        timings = get_todays_times()
        if timings:
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
        else:
            print("[WARN] No timetable found for today. Please update the timetable.")
        return

    prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    triggered_today = set()
    today = date.today()
    timings = get_todays_times()

    if timings:
        print(f"[INFO] Times for {today}: " +
              ", ".join(f"{p}={timings[p]}" for p in prayers))
    else:
        print(f"[WARN] No timetable found for {today}. Please update the timetable.")
        return

    while True:
        now_local = datetime.now(local_tz)
        current_date = now_local.date()

        if current_date != today:
            today = current_date
            triggered_today.clear()
            timings = get_todays_times()
            if timings:
                print(f"[INFO] New day times: " +
                      ", ".join(f"{p}={timings[p]}" for p in prayers))
            else:
                print(f"[WARN] No timetable for {today}. Please update.")
                return

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
