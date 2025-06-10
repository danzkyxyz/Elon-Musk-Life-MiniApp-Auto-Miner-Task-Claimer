import json
import time
import requests
from datetime import datetime, timedelta
import re
import random
import sys
from colorama import init, Fore, Style
from rich.console import Console
from rich.theme import Theme

# Initialize colorama for Windows compatibility and rich console
init(autoreset=True)
custom_theme = Theme({
    "success": "bold green",
    "error": "bold red",
    "info": "bold cyan",
    "warning": "bold yellow",
    "highlight": "bold magenta"
})
console = Console(theme=custom_theme)

# Load multiple account tokens from token.json
def load_tokens():
    try:
        with open('token.json', 'r') as file:
            data = file.read()
            lines = [line.strip() for line in data.split('\n') if line.strip()]
            accounts = []
            for i in range(0, len(lines), 2):
                token_line = lines[i]
                bear_token_line = lines[i + 1]
                if token_line.startswith('TOKEN=') and bear_token_line.startswith('BEAR_TOKEN='):
                    token = token_line.split('=')[1].strip()
                    bear_token = bear_token_line.split('=')[1].strip()
                    accounts.append({'token': token, 'bear_token': bear_token})
            console.print(f"[success]✅🔥 Loaded {len(accounts)} accounts successfully! 🚀💪[/success]")
            return accounts
    except Exception as e:
        console.print(f"[error]❌😡 Error loading tokens: {e} 🥶[/error]")
        return []

# Load proxies from proxy.txt
def load_proxies():
    try:
        with open('proxy.txt', 'r') as file:
            data = file.read()
            lines = [line.strip() for line in data.split('\n') if line.strip()]
            proxies = []
            proxy_pattern = re.compile(r'^(https?://)?(?:([^\s:]+):([^\s@]+)@)?([^\s:]+):(\d{1,5})$')
            for line in lines:
                match = proxy_pattern.match(line)
                if match:
                    protocol, username, password, host, port = match.groups()
                    protocol = protocol or 'http://'
                    proxy_url = f"{protocol}{host}:{port}"
                    if username and password:
                        proxy_url = f"{protocol}{username}:{password}@{host}:{port}"
                    proxies.append(proxy_url)
                else:
                    console.print(f"[warning]⚠️😬 Invalid proxy format skipped: {line} 🙈[/warning]")
            if not proxies:
                console.print("[warning]⚠️🌐 No valid proxies found in proxy.txt. Proceeding without proxies! 😎[/warning]")
            else:
                console.print(f"[success]✅🌍 Loaded {len(proxies)} proxies successfully! 🦄[/success]")
            return proxies
    except Exception as e:
        console.print(f"[error]❌😭 Error loading proxies: {e} 💥[/error]")
        return []

# Headers for API requests
def get_headers(token, bear_token, user_id="1824331381"):
    return {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "accept-token": token,
        "authorization": f"Bearer {bear_token}",
        "content-type": "application/json",
        "origin": "https://miniapp.elonmusklife.com",
        "priority": "u=1, i",
        "referer": "https://miniapp.elonmusklife.com/",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "user-id": user_id
    }

# Check user status
def check_user(headers, proxy=None):
    url = "https://api-miniapp.elonmusklife.com/api/user"
    try:
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
        if response.status_code == 200 and response.json().get("code") == 1:
            data = response.json()["data"]
            console.print(f"[success]👤💥 User: {data['username']} (ID: {data['user_id']}), Points: {data['point']} ⭐🔥[/success]")
            return data
        else:
            console.print(f"[error]❌😵 Failed to fetch user data: {response.json()} 😫[/error]")
            return None
    except Exception as e:
        console.print(f"[error]❌💀 Error checking user: {e} 😿[/error]")
        return None

# Check mining status
def check_mining_status(headers, proxy=None):
    url = "https://api-miniapp.elonmusklife.com/api/mining/status"
    try:
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
        if response.status_code == 200 and response.json().get("code") == 1:
            data = response.json()["data"]
            console.print(f"[info]⛏️🔍 Mining Status: {data['status']}, Reward: {data['point_reward']} 💰, Remaining Time: {data['remaining_time']} minutes ⏳🌟[/info]")
            return data
        else:
            console.print(f"[error]❌😤 Failed to check mining status: {response.json()} 😒[/error]")
            return None
    except Exception as e:
        console.print(f"[error]❌🤯 Error checking mining status: {e} 😱[/error]")
        return None

# Start mining with retry
def start_mining(headers, proxy=None, retries=3, delay=5):
    url = "https://api-miniapp.elonmusklife.com/api/mining/start"
    proxy_dict = {"http": proxy, "https": proxy} if proxy else None
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, headers=headers, proxies=proxy_dict, timeout=10)
            if response.status_code == 200 and response.json().get("code") == 1:
                data = response.json()["data"]
                console.print(f"[success]🚀💥 Mining attempt result: {data['message']}, New Balance: {data['new_balance']} 💎🔥[/success]")
                time.sleep(2)
                status = check_mining_status(headers, proxy)
                if status and status["status"] != "new":
                    console.print("[success]✅🎉 Mining confirmed active! 🦁🚀[/success]")
                    return True
                else:
                    console.print("[warning]⚠️😕 Mining status still not active after attempt! 😬[/warning]")
                    return False
            else:
                console.print(f"[error]❌🤬 Failed to start mining (Attempt {attempt}/{retries}): {response.json()} 😡[/error]")
                if attempt < retries:
                    console.print(f"[warning]⏲️😴 Retrying in {delay} seconds... 🐢[/warning]")
                    time.sleep(delay)
        except Exception as e:
            console.print(f"[error]❌💥 Error starting mining (Attempt {attempt}/{retries}): {e} 😵[/error]")
            if attempt < retries:
                console.print(f"[warning]⏲️😴 Retrying in {delay} seconds... 🐢[/warning]")
                time.sleep(delay)
    console.print("[error]❌😞 Failed to start mining after all retries. 😢[/error]")
    return False

# Get unclaimed tasks count
def get_unclaimed_tasks_count(headers, proxy=None):
    url = "https://api-miniapp.elonmusklife.com/api/user/tasks/unclaimed/count"
    try:
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
        if response.status_code == 200 and response.json().get("code") == 1:
            total = response.json()["data"]["total"]
            console.print(f"[info]📋🎯 Unclaimed tasks: {total} 🔔🔥[/info]")
            return total
        else:
            console.print(f"[error]❌😣 Failed to fetch unclaimed tasks count: {response.json()} 😩[/error]")
            return 0
    except Exception as e:
        console.print(f"[error]❌😖 Error fetching unclaimed tasks count: {e} 😷[/error]")
        return 0

# Get task list
def get_tasks(headers, proxy=None):
    url = "https://api-miniapp.elonmusklife.com/api/user/tasks"
    try:
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
        if response.status_code == 200 and response.json().get("code") == 1:
            tasks = response.json()["data"]["earns"]
            return tasks
        else:
            console.print(f"[error]❌😫 Failed to fetch tasks: {response.json()} 😾[/error]")
            return []
    except Exception as e:
        console.print(f"[error]❌😿 Error fetching tasks: {e} 😤[/error]")
        return []

# Claim task
def claim_task(headers, task, proxy=None):
    url = "https://api-miniapp.elonmusklife.com/api/user/check/task"
    payload = {
        "id": task["id"],
        "value": task["value"],
        "type": task["type"]
    }
    try:
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        response = requests.post(url, headers=headers, json=payload, proxies=proxy_dict, timeout=10)
        if response.status_code == 200 and response.json().get("code") == 1:
            data = response.json()["data"]
            console.print(f"[success]🎯🏆 Task '{task['title']}' claimed successfully! Reward: {data['point_reward']} 💰🔥[/success]")
            return True
        else:
            console.print(f"[error]❌😡 Failed to claim task '{task['title']}': {response.json()} 😣[/error]")
            return False
    except Exception as e:
        console.print(f"[error]❌😵 Error claiming task '{task['title']}': {e} 😭[/error]")
        return False

# Format seconds to HH:MM:SS
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Display countdown timer
def countdown_timer(total_seconds):
    end_time = time.time() + total_seconds
    while time.time() < end_time:
        remaining_seconds = int(end_time - time.time())
        timer_str = format_time(remaining_seconds)
        console.print(f"[info]⏲️🌟 Waiting for {timer_str} ⏳😎[/info]", end="\r")
        sys.stdout.flush()
        time.sleep(1)
    console.print(f"[info]⏲️🌟 Waiting for 00:00:00 ⏳😎[/info]")

# Process a single account
def process_account(account, proxies):
    token = account['token']
    bear_token = account['bear_token']
    proxy = random.choice(proxies) if proxies else None
    if proxy:
        console.print(f"[info]🌍🔥 Using proxy: {proxy} 🦄[/info]")
    headers = get_headers(token, bear_token)
    
    user_data = check_user(headers, proxy)
    if not user_data:
        console.print("[error]❌😞 Skipping account due to user check failure. 😢[/error]")
        return
    
    console.print(f"[highlight]⏰💥 [{datetime.now()}] Starting cycle for account: {user_data['username']} 🚀🦁[/highlight]")
    
    mining_status = check_mining_status(headers, proxy)
    if mining_status and mining_status["status"] == "new":
        start_mining(headers, proxy)
    elif mining_status and mining_status["status"] == "cooldown":
        console.print(f"[warning]⏳😴 Mining on cooldown. Remaining time: {mining_status['remaining_time']} minutes 🐢[/warning]")
    else:
        console.print("[warning]⚠️😕 Mining status unknown or not ready to start. 😬[/warning]")
    
    unclaimed_count = get_unclaimed_tasks_count(headers, proxy)
    if unclaimed_count > 0:
        tasks = get_tasks(headers, proxy)
        for task in tasks:
            if not task["is_active"]:
                claim_task(headers, task, proxy)
    
    console.print("[highlight]🔄💥 Start mining again! 🚀🔥[/highlight]")
    mining_status = check_mining_status(headers, proxy)
    if mining_status and mining_status["status"] == "new":
        start_mining(headers, proxy)
    elif mining_status and mining_status["status"] == "cooldown":
        console.print(f"[warning]⏳😴 Mining on cooldown. Remaining time: {mining_status['remaining_time']} minutes 🐢[/warning]")
    else:
        console.print("[warning]⚠️😕 Mining status unknown or not ready to start. 😬[/warning]")
    
    user_data = check_user(headers, proxy)
    if user_data:
        console.print(f"[success]💰🎉 Total points: {user_data['point']} 🏆🔥[/success]")

# Main loop
def main():
    accounts = load_tokens()
    if not accounts:
        console.print("[error]❌😡 No accounts defined. Ensure token.json exists and is correctly formatted. 😢[/error]")
        return
    
    proxies = load_proxies()
    
    interval = (4 * 60 * 60) + 60  # 4 hours + 1 minute in seconds

    while True:
        for i, account in enumerate(accounts, 1):
            console.print(f"[highlight]🔥🎉 === Processing Account {i} of {len(accounts)} === 💥🦄[/highlight]")
            process_account(account, proxies)
        
        countdown_timer(interval)

if __name__ == "__main__":
    console.print("[success]🌟🔥 Starting Auto Mining Script! Yooo, let's rock it! 🚀🦁[/success]")
    try:
        main()
    except KeyboardInterrupt:
        console.print("[warning]🛑😎 Script stopped by user. Peace out! 👋[/warning]")
    except Exception as e:
        console.print(f"[error]❌😵 Unexpected error: {e} 😭[/error]")