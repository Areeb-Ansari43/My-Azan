import os
import requests
import time
from datetime import datetime, date
import pytz

local_tz = pytz.timezone("Europe/London")

# October 2026 - Farley Hill Jame Masjid (start times, 24-hour, UK local time)
TIMETABLE = {
    (2026, 10, 1): {"Fajr": "05:29", "Dhuhr": "12:56", "Asr": "16:43", "Maghrib": "18:44", "Isha": "19:58"},
    (2026, 10, 2): {"Fajr": "05:30", "Dhuhr": "12:56", "Asr": "16:41", "Maghrib": "18:41", "Isha": "19:56"},
    (2026, 10, 3): {"Fajr": "05:32", "Dhuhr": "12:56", "Asr": "16:39", "Maghrib": "18:39", "Isha": "19:54"},
    (2026, 10, 4): {"Fajr": "05:34", "Dhuhr": "12:55", "Asr": "16:37", "Maghrib": "18:37", "Isha": "19:52"},
    (2026, 10, 5): {"Fajr": "05:35", "Dhuhr": "12:55", "Asr": "16:35", "Maghrib": "18:35", "Isha": "19:50"},
    (2026, 10, 6): {"Fajr": "05:37", "Dhuhr": "12:55", "Asr": "16:33", "Maghrib": "18:32", "Isha": "19:47"},
    (2026, 10, 7): {"Fajr": "05:38", "Dhuhr": "12:54", "Asr": "16:31", "Maghrib": "18:30", "Isha": "19:45"},
    (2026, 10, 8): {"Fajr": "05:40", "Dhuhr": "12:54", "Asr": "16:29", "Maghrib": "18:28", "Isha": "19:43"},
    (2026, 10, 9): {"Fajr": "05:41", "Dhuhr": "12:54", "Asr": "16:27", "Maghrib": "18:26", "Isha": "19:41"},
    (2026, 10, 10): {"Fajr": "05:43", "Dhuhr": "12:54", "Asr": "16:25", "Maghrib": "18:23", "Isha": "19:38"},
    (2026, 10, 11): {"Fajr": "05:45", "Dhuhr": "12:53", "Asr": "16:23", "Maghrib": "18:21", "Isha": "19:36"},
    (2026, 10, 12): {"Fajr": "05:46", "Dhuhr": "12:53", "Asr": "16:21", "Maghrib": "18:19", "Isha": "19:34"},
    (2026, 10, 13): {"Fajr": "05:48", "Dhuhr": "12:53", "Asr": "16:19", "Maghrib": "18:17", "Isha": "19:32"},
    (2026, 10, 14): {"Fajr": "05:50", "Dhuhr": "12:53", "Asr": "16:17", "Maghrib": "18:15", "Isha": "19:30"},
    (2026, 10, 15): {"Fajr": "05:51", "Dhuhr": "12:52", "Asr": "16:15", "Maghrib": "18:12", "Isha": "19:27"},
    (2026, 10, 16): {"Fajr": "05:53", "Dhuhr": "12:52", "Asr": "16:13", "Maghrib": "18:10", "Isha": "19:25"},
    (2026, 10, 17): {"Fajr": "05:54", "Dhuhr": "12:52", "Asr": "16:11", "Maghrib": "18:08", "Isha": "19:23"},
    (2026, 10, 18): {"Fajr": "05:56", "Dhuhr": "12:52", "Asr": "16:09", "Maghrib": "18:06", "Isha": "19:21"},
    (2026, 10, 19): {"Fajr": "05:58", "Dhuhr": "12:52", "Asr": "16:07", "Maghrib": "18:04", "Isha": "19:19"},
    (2026, 10, 20): {"Fajr": "05:59", "Dhuhr": "12:51", "Asr": "16:05", "Maghrib": "18:02", "Isha": "19:17"},
    (2026, 10, 21): {"Fajr": "06:01", "Dhuhr": "12:51", "Asr": "16:04", "Maghrib": "18:00", "Isha": "19:15"},
    (2026, 10, 22): {"Fajr": "06:03", "Dhuhr": "12:51", "Asr": "16:02", "Maghrib": "17:58", "Isha": "19:13"},
    (2026, 10, 23): {"Fajr": "06:04", "Dhuhr": "12:51", "Asr": "16:00", "Maghrib": "17:56", "Isha": "19:11"},
    (2026, 10, 24): {"Fajr": "06:06", "Dhuhr": "12:51", "Asr": "15:58", "Maghrib": "17:54", "Isha": "19:09"},
    (2026, 10, 25): {"Fajr": "05:08", "Dhuhr": "11:51", "Asr": "14:56", "Maghrib": "16:52", "Isha": "18:07"},
    (2026, 10, 26): {"Fajr": "05:09", "Dhuhr": "11:51", "Asr": "14:54", "Maghrib": "16:50", "Isha": "18:05"},
    (2026, 10, 27): {"Fajr": "05:11", "Dhuhr": "11:51", "Asr": "14:52", "Maghrib": "16:48", "Isha": "18:03"},
    (2026, 10, 28): {"Fajr": "05:13", "Dhuhr": "11:50", "Asr": "14:51", "Maghrib": "16:46", "Isha": "18:01"},
    (2026, 10, 29): {"Fajr": "05:14", "Dhuhr": "11:50", "Asr": "14:49", "Maghrib": "16:44", "Isha": "17:59"},
    (2026, 10, 30): {"Fajr": "05:16", "Dhuhr": "11:50", "Asr": "14:47", "Maghrib": "16:42", "Isha": "17:57"},
    (2026, 10, 31): {"Fajr": "05:18", "Dhuhr": "11:50", "Asr": "14:45", "Maghrib": "16:40", "Isha": "17:55"},
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
