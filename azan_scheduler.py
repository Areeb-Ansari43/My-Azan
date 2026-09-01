import os
import requests
import time
from datetime import datetime, date
import pytz

local_tz = pytz.timezone("Europe/London")

TIMETABLE = {
    (2026, 9, 1):  {"Fajr": "04:35", "Dhuhr": "13:07", "Asr": "17:41", "Maghrib": "19:53", "Isha": "21:05"},
    (2026, 9, 2):  {"Fajr": "04:37", "Dhuhr": "13:06", "Asr": "17:39", "Maghrib": "19:51", "Isha": "21:03"},
    (2026, 9, 3):  {"Fajr": "04:39", "Dhuhr": "13:06", "Asr": "17:37", "Maghrib": "19:49", "Isha": "21:01"},
    (2026, 9, 4):  {"Fajr": "04:41", "Dhuhr": "13:06", "Asr": "17:36", "Maghrib": "19:46", "Isha": "20:58"},
    (2026, 9, 5):  {"Fajr": "04:43", "Dhuhr": "13:05", "Asr": "17:34", "Maghrib": "19:44", "Isha": "20:56"},
    (2026, 9, 6):  {"Fajr": "04:45", "Dhuhr": "13:05", "Asr": "17:32", "Maghrib": "19:42", "Isha": "20:54"},
    (2026, 9, 7):  {"Fajr": "04:47", "Dhuhr": "13:05", "Asr": "17:30", "Maghrib": "19:39", "Isha": "20:51"},
    (2026, 9, 8):  {"Fajr": "04:49", "Dhuhr": "13:04", "Asr": "17:28", "Maghrib": "19:37", "Isha": "20:49"},
    (2026, 9, 9):  {"Fajr": "04:51", "Dhuhr": "13:04", "Asr": "17:27", "Maghrib": "19:35", "Isha": "20:47"},
    (2026, 9, 10): {"Fajr": "04:52", "Dhuhr": "13:04", "Asr": "17:25", "Maghrib": "19:33", "Isha": "20:45"},
    (2026, 9, 11): {"Fajr": "04:54", "Dhuhr": "13:03", "Asr": "17:23", "Maghrib": "19:30", "Isha": "20:42"},
    (2026, 9, 12): {"Fajr": "04:56", "Dhuhr": "13:03", "Asr": "17:21", "Maghrib": "19:28", "Isha": "20:40"},
    (2026, 9, 13): {"Fajr": "04:58", "Dhuhr": "13:02", "Asr": "17:19", "Maghrib": "19:26", "Isha": "20:38"},
    (2026, 9, 14): {"Fajr": "05:00", "Dhuhr": "13:02", "Asr": "17:17", "Maghrib": "19:23", "Isha": "20:35"},
    (2026, 9, 15): {"Fajr": "05:02", "Dhuhr": "13:02", "Asr": "17:15", "Maghrib": "19:21", "Isha": "20:33"},
    (2026, 9, 16): {"Fajr": "05:04", "Dhuhr": "13:01", "Asr": "17:13", "Maghrib": "19:19", "Isha": "20:31"},
    (2026, 9, 17): {"Fajr": "05:06", "Dhuhr": "13:01", "Asr": "17:11", "Maghrib": "19:16", "Isha": "20:28"},
    (2026, 9, 18): {"Fajr": "05:08", "Dhuhr": "13:01", "Asr": "17:09", "Maghrib": "19:14", "Isha": "20:26"},
    (2026, 9, 19): {"Fajr": "05:10", "Dhuhr": "13:00", "Asr": "17:07", "Maghrib": "19:12", "Isha": "20:24"},
    (2026, 9, 20): {"Fajr": "05:11", "Dhuhr": "13:00", "Asr": "17:05", "Maghrib": "19:09", "Isha": "20:21"},
    (2026, 9, 21): {"Fajr": "05:13", "Dhuhr": "13:00", "Asr": "17:03", "Maghrib": "19:07", "Isha": "20:19"},
    (2026, 9, 22): {"Fajr": "05:15", "Dhuhr": "12:59", "Asr": "17:01", "Maghrib": "19:05", "Isha": "20:17"},
    (2026, 9, 23): {"Fajr": "05:16", "Dhuhr": "12:59", "Asr": "16:59", "Maghrib": "19:02", "Isha": "20:15"},
    (2026, 9, 24): {"Fajr": "05:18", "Dhuhr": "12:59", "Asr": "16:57", "Maghrib": "19:00", "Isha": "20:13"},
    (2026, 9, 25): {"Fajr": "05:19", "Dhuhr": "12:58", "Asr": "16:55", "Maghrib": "18:58", "Isha": "20:11"},
    (2026, 9, 26): {"Fajr": "05:21", "Dhuhr": "12:58", "Asr": "16:53", "Maghrib": "18:55", "Isha": "20:08"},
    (2026, 9, 27): {"Fajr": "05:23", "Dhuhr": "12:58", "Asr": "16:51", "Maghrib": "18:53", "Isha": "20:06"},
    (2026, 9, 28): {"Fajr": "05:24", "Dhuhr": "12:57", "Asr": "16:49", "Maghrib": "18:51", "Isha": "20:04"},
    (2026, 9, 29): {"Fajr": "05:26", "Dhuhr": "12:57", "Asr": "16:47", "Maghrib": "18:48", "Isha": "20:02"},
    (2026, 9, 30): {"Fajr": "05:27", "Dhuhr": "12:57", "Asr": "16:45", "Maghrib": "18:46", "Isha": "20:00"},
}

def get_todays_times():
    now = datetime.now(local_tz)
    key = (now.year, now.month, now.day)
    return TIMETABLE.get(key, None)

def trigger_voice_monkey(prayer_name, prayer_time):
    token = os.environ.get("VOICE_MONKEY_TOKEN")
    
    if not token:
        print("[WARN] VOICE_MONKEY_TOKEN secret not set")
        return
    
    device_id = "azanlutontrigger"
    
    try:
        url = f"https://api-v2.voicemonkey.io/trigger?token={token}&device={device_id}"
        resp = requests.get(url, timeout=10)
        print(f"[INFO] Voice Monkey triggered for {prayer_name} at {prayer_time}. Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"[SUCCESS] Azan should now play for {prayer_name}")
    except Exception as e:
        print(f"[ERROR] Voice Monkey failed: {e}")

def run():
    now = datetime.now(local_tz)

    # Manual dispatch for testing
    if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        print("[INFO] Manual dispatch — testing Voice Monkey trigger")
        trigger_voice_monkey("Test", "now")
        return

    # Main loop
    prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    triggered_today = set()
    today = date.today()
    timings = get_todays_times()

    if timings:
        print(f"[INFO] Times for {today}: " + ", ".join(f"{p}={timings[p]}" for p in prayers))
    else:
        print(f"[WARN] No timetable found for {today}")
        return

    while True:
        now_local = datetime.now(local_tz)
        current_date = now_local.date()

        if current_date != today:
            today = current_date
            triggered_today.clear()
            timings = get_todays_times()
            if timings:
                print(f"[INFO] New day times: " + ", ".join(f"{p}={timings[p]}" for p in prayers))
            else:
                print(f"[WARN] No timetable for {today}")
                return

        if timings:
            current_time_str = now_local.strftime("%H:%M")
            for prayer in prayers:
                if current_time_str == timings[prayer] and prayer not in triggered_today:
                    print(f"[INFO] {prayer} at {timings[prayer]} — triggering Azan")
                    trigger_voice_monkey(prayer, timings[prayer])
                    triggered_today.add(prayer)
                    time.sleep(61)
                    break

        time.sleep(30)

if __name__ == "__main__":
    run()
