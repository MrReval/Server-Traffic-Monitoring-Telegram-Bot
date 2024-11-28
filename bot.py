import re
import subprocess
import time
import requests
import os

BOT_TOKEN = "BOT_TOKEN"
CHAT_ID = "CHAT_ID" 
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

server = "Server One"

def check_and_install_vnstat():
    try:
        subprocess.run(["vnstat", "--version"], capture_output=True, text=True, check=True)
        print("vnstat is already installed.")
    except subprocess.CalledProcessError:
        print("vnstat is not installed. Installing...")
        subprocess.run(["sudo", "apt", "install", "vnstat", "-y"], check=True)
        print("vnstat has been installed.")
        
        subprocess.run(["sudo", "systemctl", "start", "vnstat"], check=True)
        print("vnstat has started.")
        
        subprocess.run(["sudo", "systemctl", "enable", "vnstat"], check=True)
        print("vnstat has been enabled.")

def get_vnstat_output(): 
    try:
        result = subprocess.run(["vnstat", "-s"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error running vnstat:", e)
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
            print(f"Error sending message: {response.text}")
    except requests.RequestException as e:
        print(f"Network error: {e}")

def send_traffic_report():
    vnstat_output = get_vnstat_output()
    if vnstat_output:
        rx, tx, total = extract_traffic_data(vnstat_output)
        if rx and tx and total:
            message = f"\ud83d\uded1| Traffic Report for {server}:\n\n \ud83d\udce5 - Incoming Traffic: \n {rx}\n \ud83d\udce4 - Outgoing Traffic: \n {tx}\n \ud83d\udcca - Total Traffic: \n {total}"
        else:
            message = "Error extracting traffic data."
        send_message_to_telegram(message)

if __name__ == "__main__":
    check_and_install_vnstat() 
    while True:
        send_traffic_report()
        time.sleep(3600)
