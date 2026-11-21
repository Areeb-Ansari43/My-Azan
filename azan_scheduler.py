import os
import requests
import time
from datetime import datetime, date
import pytz

local_tz = pytz.timezone("Europe/London")

# November 2026 - Farley Hill Jame Masjid (start times, 24-hour, UK local time)
TIMETABLE = {
    (2026, 11, 1): {"Fajr": "05:20", "Asr": "14:44", "Maghrib": "16:38", "Isha": "18:00"},
    (2026, 11, 2): {"Fajr": "05:21", "Asr": "14:42", "Maghrib": "16:36", "Isha": "17:58"},
    (2026, 11, 3): {"Fajr": "05:23", "Asr": "14:40", "Maghrib": "16:35", "Isha": "17:57"},
    (2026, 11, 4): {"Fajr": "05:25", "Asr": "14:39", "Maghrib": "16:33", "Isha": "17:55"},
    (2026, 11, 5): {"Fajr": "05:26", "Asr": "14:37", "Maghrib": "16:31", "Isha": "17:54"},
    (2026, 11, 6): {"Fajr": "05:28", "Asr": "14:35", "Maghrib": "16:29", "Isha": "17:52"},
    (2026, 11, 7): {"Fajr": "05:30", "Asr": "14:34", "Maghrib": "16:28", "Isha": "17:51"},
    (2026, 11, 8): {"Fajr": "05:31", "Asr": "14:32", "Maghrib": "16:26", "Isha": "17:50"},
    (2026, 11, 9): {"Fajr": "05:33", "Asr": "14:31", "Maghrib": "16:24", "Isha": "17:48"},
    (2026, 11, 10): {"Fajr": "05:35", "Asr": "14:29", "Maghrib": "16:23", "Isha": "17:47"},
    (2026, 11, 11): {"Fajr": "05:36", "Asr": "14:28", "Maghrib": "16:21", "Isha": "17:46"},
    (2026, 11, 12): {"Fajr": "05:38", "Asr": "14:26", "Maghrib": "16:20", "Isha": "17:44"},
    (2026, 11, 13): {"Fajr": "05:40", "Asr": "14:25", "Maghrib": "16:18", "Isha": "17:43"},
    (2026, 11, 14): {"Fajr": "05:41", "Asr": "14:24", "Maghrib": "16:17", "Isha": "17:42"},
    (2026, 11, 15): {"Fajr": "05:43", "Asr": "14:22", "Maghrib": "16:16", "Isha": "17:41"},
    (2026, 11, 16): {"Fajr": "05:45", "Asr": "14:21", "Maghrib": "16:14", "Isha": "17:40"},
    (2026, 11, 17): {"Fajr": "05:46", "Asr": "14:20", "Maghrib": "16:13", "Isha": "17:39"},
    (2026, 11, 18): {"Fajr": "05:48", "Asr": "14:19", "Maghrib": "16:12", "Isha": "17:38"},
    (2026, 11, 19): {"Fajr": "05:49", "Asr": "14:18", "Maghrib": "16:10", "Isha": "17:37"},
    (2026, 11, 20): {"Fajr": "05:51", "Asr": "14:16", "Maghrib": "16:09", "Isha": "17:36"},
    (2026, 11, 21): {"Fajr": "05:53", "Asr": "14:15", "Maghrib": "16:08", "Isha": "17:35"},
    (2026, 11, 22): {"Fajr": "05:54", "Asr": "14:14", "Maghrib": "16:07", "Isha": "17:34"},
    (2026, 11, 23): {"Fajr": "05:56", "Asr": "14:13", "Maghrib": "16:06", "Isha": "17:33"},
    (2026, 11, 24): {"Fajr": "05:57", "Asr": "14:12", "Maghrib": "16:05", "Isha": "17:32"},
    (2026, 11, 25): {"Fajr": "05:59", "Asr": "14:12", "Maghrib": "16:04", "Isha": "17:32"},
    (2026, 11, 26): {"Fajr": "06:00", "Asr": "14:11", "Maghrib": "16:03", "Isha": "17:31"},
    (2026, 11, 27): {"Fajr": "06:02", "Asr": "14:10", "Maghrib": "16:02", "Isha": "17:30"},
    (2026, 11, 28): {"Fajr": "06:03", "Asr": "14:09", "Maghrib": "16:01", "Isha": "17:30"},
    (2026, 11, 29): {"Fajr": "06:04", "Asr": "14:09", "Maghrib": "16:01", "Isha": "17:29"},
    (2026, 11, 30): {"Fajr": "06:06", "Asr": "14:08", "Maghrib": "16:00", "Isha": "17:29"},
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
    prayers = ["Fajr", "Asr", "Maghrib", "Isha"]
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
