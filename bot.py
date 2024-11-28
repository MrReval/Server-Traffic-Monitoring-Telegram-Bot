import re
import subprocess
import time
import requests
import os

BOT_TOKEN = "BOT_TOKEN"
CHAT_ID = "CHAT_ID" 
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

server = "سرور یک"

def check_and_install_vnstat():
    try:
        subprocess.run(["vnstat", "--version"], capture_output=True, text=True, check=True)
        print("vnstat قبلاً نصب شده است.")
    except subprocess.CalledProcessError:
        print("vnstat نصب نشده است. در حال نصب...")
        subprocess.run(["sudo", "apt", "install", "vnstat", "-y"], check=True)
        print("vnstat نصب شد.")
        
        subprocess.run(["sudo", "systemctl", "start", "vnstat"], check=True)
        print("vnstat شروع شد.")
        
        subprocess.run(["sudo", "systemctl", "enable", "vnstat"], check=True)
        print("vnstat فعال شد.")

def get_vnstat_output(): 
    try:
        result = subprocess.run(["vnstat", "-s"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("خطا در اجرای vnstat:", e)
        return None

def extract_traffic_data(vnstat_output):
    pattern = r"(\d+\.\d+\s[KMG]iB)\s+/\s+(\d+\.\d+\s[KMG]iB)\s+/\s+(\d+\.\d+\s[KMG]iB)"
    match = re.search(pattern, vnstat_output)
    if match:
        rx = match.group(1)
        tx = match.group(2)
        total = match.group(3)
        return rx, tx, total
    return None, None, None

def send_message_to_telegram(message):
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(TELEGRAM_API_URL, json=payload)
        if response.status_code != 200:
            print(f"خطا در ارسال پیام: {response.text}")
    except requests.RequestException as e:
        print(f"خطای شبکه: {e}")

def send_traffic_report():
    vnstat_output = get_vnstat_output()
    if vnstat_output:
        rx, tx, total = extract_traffic_data(vnstat_output)
        if rx and tx and total:
            message = f"🛑| گزارش ترافیک {server}:\n\n 📥 - ترافیک دریافتی: \n {rx}\n 📤- ترافیک ارسالی: \n {tx}\n 📊- کل ترافیک: \n {total}"
        else:
            message = "خطا در استخراج داده‌های ترافیک."
        send_message_to_telegram(message)

if __name__ == "__main__":
    check_and_install_vnstat() 
    while True:
        send_traffic_report()
        time.sleep(3600) 
