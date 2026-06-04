import os
import requests
import time
from datetime import datetime, date
import pytz

local_tz = pytz.timezone("Europe/London")

TIMETABLE = {
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
