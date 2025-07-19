import psutil
import time
from pync import Notifier

# Track if we've already notified
notified_low = False
notified_high = False
# print("Checking battery info...")
# battery = psutil.sensors_battery()
# print("Battery object:", battery)
def send_notification(title, message):
    print(f"Notification: {title} - {message}")
    Notifier.notify(message, title=title)

send_notification("🔋 Battery Charged", "Battery 100%. Consider unplugging.")

while True:
    battery = psutil.sensors_battery()

    if battery is None:
        print("Battery info not available.")
        break

    percent = battery.percent
    charging = battery.power_plugged

    # Notify when battery is low (15% or less)
    if percent <= 15 and not charging and not notified_low:
        send_notification("⚠️ Battery Low", f"Battery at {percent}%. Plug in the charger.")
        notified_low = True
        notified_high = False  # reset other flag

    # Notify when battery reaches 90% while charging
    elif percent >= 90 and charging and not notified_high:
        send_notification("🔋 Battery Charged", f"Battery at {percent}%. Consider unplugging.")
        notified_high = True
        notified_low = False  # reset other flag

    # Reset notifications when outside trigger zone
    if percent > 15 and not charging:
        notified_low = False
    if percent < 90 and charging:
        notified_high = False

    time.sleep(60)  # check every minute
