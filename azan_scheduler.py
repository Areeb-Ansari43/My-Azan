import os
import requests
import time
from datetime import datetime, date
import pytz

local_tz = pytz.timezone("Europe/London")

TIMETABLE = {
    (2026, 7, 1):  {"Fajr": "02:49", "Dhuhr": "13:11", "Asr": "18:43", "Maghrib": "21:29", "Isha": "22:41"},
    (2026, 7, 2):  {"Fajr": "02:50", "Dhuhr": "13:11", "Asr": "18:43", "Maghrib": "21:29", "Isha": "22:41"},
    (2026, 7, 3):  {"Fajr": "02:51", "Dhuhr": "13:11", "Asr": "18:43", "Maghrib": "21:28", "Isha": "22:40"},
    (2026, 7, 4):  {"Fajr": "02:52", "Dhuhr": "13:11", "Asr": "18:42", "Maghrib": "21:28", "Isha": "22:40"},
    (2026, 7, 5):  {"Fajr": "02:54", "Dhuhr": "13:11", "Asr": "18:42", "Maghrib": "21:27", "Isha": "22:39"},
    (2026, 7, 6):  {"Fajr": "02:56", "Dhuhr": "13:12", "Asr": "18:42", "Maghrib": "21:27", "Isha": "22:39"},
    (2026, 7, 7):  {"Fajr": "02:57", "Dhuhr": "13:12", "Asr": "18:42", "Maghrib": "21:26", "Isha": "22:38"},
    (2026, 7, 8):  {"Fajr": "02:58", "Dhuhr": "13:12", "Asr": "18:41", "Maghrib": "21:25", "Isha": "22:37"},
    (2026, 7, 9):  {"Fajr": "02:59", "Dhuhr": "13:12", "Asr": "18:41", "Maghrib": "21:25", "Isha": "22:37"},
    (2026, 7, 10): {"Fajr": "03:01", "Dhuhr": "13:12", "Asr": "18:41", "Maghrib": "21:24", "Isha": "22:36"},
    (2026, 7, 11): {"Fajr": "03:02", "Dhuhr": "13:12", "Asr": "18:40", "Maghrib": "21:23", "Isha": "22:35"},
    (2026, 7, 12): {"Fajr": "03:04", "Dhuhr": "13:12", "Asr": "18:40", "Maghrib": "21:22", "Isha": "22:34"},
    (2026, 7, 13): {"Fajr": "03:05", "Dhuhr": "13:13", "Asr": "18:39", "Maghrib": "21:21", "Isha": "22:33"},
    (2026, 7, 14): {"Fajr": "03:07", "Dhuhr": "13:13", "Asr": "18:39", "Maghrib": "21:20", "Isha": "22:32"},
    (2026, 7, 15): {"Fajr": "03:08", "Dhuhr": "13:13", "Asr": "18:38", "Maghrib": "21:19", "Isha": "22:31"},
    (2026, 7, 16): {"Fajr": "03:10", "Dhuhr": "13:13", "Asr": "18:38", "Maghrib": "21:18", "Isha": "22:30"},
    (2026, 7, 17): {"Fajr": "03:11", "Dhuhr": "13:13", "Asr": "18:37", "Maghrib": "21:17", "Isha": "22:29"},
    (2026, 7, 18): {"Fajr": "03:13", "Dhuhr": "13:13", "Asr": "18:37", "Maghrib": "21:16", "Isha": "22:28"},
    (2026, 7, 19): {"Fajr": "03:14", "Dhuhr": "13:13", "Asr": "18:36", "Maghrib": "21:15", "Isha": "22:27"},
    (2026, 7, 20): {"Fajr": "03:16", "Dhuhr": "13:13", "Asr": "18:36", "Maghrib": "21:14", "Isha": "22:26"},
    (2026, 7, 21): {"Fajr": "03:18", "Dhuhr": "13:13", "Asr": "18:35", "Maghrib": "21:12", "Isha": "22:24"},
    (2026, 7, 22): {"Fajr": "03:19", "Dhuhr": "13:13", "Asr": "18:34", "Maghrib": "21:11", "Isha": "22:23"},
    (2026, 7, 23): {"Fajr": "03:21", "Dhuhr": "13:13", "Asr": "18:33", "Maghrib": "21:10", "Isha": "22:22"},
    (2026, 7, 24): {"Fajr": "03:23", "Dhuhr": "13:13", "Asr": "18:32", "Maghrib": "21:08", "Isha": "22:20"},
    (2026, 7, 25): {"Fajr": "03:25", "Dhuhr": "13:13", "Asr": "18:32", "Maghrib": "21:07", "Isha": "22:19"},
    (2026, 7, 26): {"Fajr": "03:26", "Dhuhr": "13:13", "Asr": "18:31", "Maghrib": "21:05", "Isha": "22:17"},
    (2026, 7, 27): {"Fajr": "03:28", "Dhuhr": "13:13", "Asr": "18:30", "Maghrib": "21:03", "Isha": "22:15"},
    (2026, 7, 28): {"Fajr": "03:30", "Dhuhr": "13:13", "Asr": "18:29", "Maghrib": "21:01", "Isha": "22:13"},
    (2026, 7, 29): {"Fajr": "03:32", "Dhuhr": "13:13", "Asr": "18:28", "Maghrib": "20:59", "Isha": "22:11"},
    (2026, 7, 30): {"Fajr": "03:34", "Dhuhr": "13:13", "Asr": "18:27", "Maghrib": "20:58", "Isha": "22:10"},
    (2026, 7, 31): {"Fajr": "03:36", "Dhuhr": "13:13", "Asr": "18:26", "Maghrib": "20:57", "Isha": "22:09"},
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
