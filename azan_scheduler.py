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
    # May 2026
    (2026, 5, 1):  {"Fajr": "03:47", "Dhuhr": "13:04", "Asr": "18:06", "Maghrib": "20:29", "Isha": "21:39"},
    (2026, 5, 2):  {"Fajr": "03:44", "Dhuhr": "13:04", "Asr": "18:07", "Maghrib": "20:31", "Isha": "21:40"},
    (2026, 5, 3):  {"Fajr": "03:42", "Dhuhr": "13:04", "Asr": "18:08", "Maghrib": "20:33", "Isha": "21:42"},
    (2026, 5, 4):  {"Fajr": "03:40", "Dhuhr": "13:03", "Asr": "18:09", "Maghrib": "20:34", "Isha": "21:43"},
    (2026, 5, 5):  {"Fajr": "03:38", "Dhuhr": "13:03", "Asr": "18:10", "Maghrib": "20:36", "Isha": "21:44"},
    (2026, 5, 6):  {"Fajr": "03:36", "Dhuhr": "13:03", "Asr": "18:11", "Maghrib": "20:38", "Isha": "21:46"},
    (2026, 5, 7):  {"Fajr": "03:34", "Dhuhr": "13:03", "Asr": "18:12", "Maghrib": "20:39", "Isha": "21:47"},
    (2026, 5, 8):  {"Fajr": "03:32", "Dhuhr": "13:03", "Asr": "18:13", "Maghrib": "20:41", "Isha": "21:49"},
    (2026, 5, 9):  {"Fajr": "03:30", "Dhuhr": "13:03", "Asr": "18:14", "Maghrib": "20:42", "Isha": "21:51"},
    (2026, 5, 10): {"Fajr": "03:28", "Dhuhr": "13:03", "Asr": "18:15", "Maghrib": "20:44", "Isha": "21:53"},
    (2026, 5, 11): {"Fajr": "03:25", "Dhuhr": "13:03", "Asr": "18:16", "Maghrib": "20:46", "Isha": "21:56"},
    (2026, 5, 12): {"Fajr": "03:23", "Dhuhr": "13:03", "Asr": "18:17", "Maghrib": "20:47", "Isha": "21:58"},
    (2026, 5, 13): {"Fajr": "03:21", "Dhuhr": "13:03", "Asr": "18:18", "Maghrib": "20:49", "Isha": "22:00"},
    (2026, 5, 14): {"Fajr": "03:19", "Dhuhr": "13:03", "Asr": "18:19", "Maghrib": "20:50", "Isha": "22:01"},
    (2026, 5, 15): {"Fajr": "03:17", "Dhuhr": "13:03", "Asr": "18:20", "Maghrib": "20:52", "Isha": "22:03"},
    (2026, 5, 16): {"Fajr": "03:16", "Dhuhr": "13:03", "Asr": "18:21", "Maghrib": "20:53", "Isha": "22:05"},
    (2026, 5, 17): {"Fajr": "03:14", "Dhuhr": "13:03", "Asr": "18:21", "Maghrib": "20:55", "Isha": "22:07"},
    (2026, 5, 18): {"Fajr": "03:12", "Dhuhr": "13:03", "Asr": "18:22", "Maghrib": "20:56", "Isha": "22:09"},
    (2026, 5, 19): {"Fajr": "03:10", "Dhuhr": "13:03", "Asr": "18:23", "Maghrib": "20:58", "Isha": "22:11"},
    (2026, 5, 20): {"Fajr": "03:09", "Dhuhr": "13:03", "Asr": "18:24", "Maghrib": "20:59", "Isha": "22:12"},
    (2026, 5, 21): {"Fajr": "03:08", "Dhuhr": "13:03", "Asr": "18:25", "Maghrib": "21:01", "Isha": "22:13"},
    (2026, 5, 22): {"Fajr": "03:07", "Dhuhr": "13:03", "Asr": "18:26", "Maghrib": "21:02", "Isha": "22:15"},
    (2026, 5, 23): {"Fajr": "03:05", "Dhuhr": "13:03", "Asr": "18:26", "Maghrib": "21:03", "Isha": "22:16"},
    (2026, 5, 24): {"Fajr": "03:04", "Dhuhr": "13:04", "Asr": "18:27", "Maghrib": "21:05", "Isha": "22:18"},
    (2026, 5, 25): {"Fajr": "03:02", "Dhuhr": "13:04", "Asr": "18:28", "Maghrib": "21:06", "Isha": "22:20"},
    (2026, 5, 26): {"Fajr": "03:01", "Dhuhr": "13:04", "Asr": "18:29", "Maghrib": "21:07", "Isha": "22:21"},
    (2026, 5, 27): {"Fajr": "02:59", "Dhuhr": "13:04", "Asr": "18:30", "Maghrib": "21:09", "Isha": "22:23"},
    (2026, 5, 28): {"Fajr": "02:58", "Dhuhr": "13:04", "Asr": "18:30", "Maghrib": "21:10", "Isha": "22:24"},
    (2026, 5, 29): {"Fajr": "02:57", "Dhuhr": "13:04", "Asr": "18:31", "Maghrib": "21:11", "Isha": "22:26"},
    (2026, 5, 30): {"Fajr": "02:56", "Dhuhr": "13:04", "Asr": "18:32", "Maghrib": "21:12", "Isha": "22:27"},
    (2026, 5, 31): {"Fajr": "02:54", "Dhuhr": "13:04", "Asr": "18:32", "Maghrib": "21:13", "Isha": "22:29"},
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
