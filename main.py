#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: github.com/imvast
@Date: 2/5/2023
"""
import concurrent.futures
import random
import time
import requests
import os

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    # ...
]
def add_random_delay(max_delay):
    delay = random.uniform(4, max_delay)
    time.sleep(delay)
with open("proxies.txt","r+", encoding="utf-8") as f:
    prox = [i.strip() for i in f.readlines()]
    proxies = []
    for i in prox:
        if i != None and i != "":
            proxies.append(i)

def get_key():
	with open("keys.txt", 'r') as f:
		keys = [line.strip() for line in f.readlines()]
	return keys
            
def worker(key, user_agent, proxy_type, proxy):
	try:
		response = requests.post("https://api.capmonster.cloud/getBalance", json={ "clientKey": key}, headers={'User-Agent': user_agent}, proxies={proxy_type: proxy}, timeout=5)
		checkResp = response.json()
		if response.status_code == 200:
			balance = checkResp.get('balance')
			print(f"[+] Valid Key: {key} | Balance: {balance}")
		elif checkResp.get('errorCode') == "ERROR_KEY_DOES_NOT_EXIST":
			print(f"[-] Invalid Key: {key}")
		else:
			print(f"[!] Error checking key: {key} | {response.status_code} | {checkResp}")
			
	except Exception as e:
		print(f"[ERROR] Exception in worker -> {e}")
		
def main():
	keys = get_key()
	user_agent = random.choice(user_agents)
	proxy = proxy = random.choice(proxies)
	print("What Proxy to use(1-http, 2-https, 3-socks5)")
	inp = int(input(":$"))
	if inp == 1:
		proxy_type = "http"
		try:
			with concurrent.futures.ThreadPoolExecutor() as executor:
				futures = [executor.submit(worker, key, user_agent, proxy_type, proxy) for key in keys]
		except:
			os._exit(0)
	elif inp == 2:
		proxy_type = "https"
		try:
			with concurrent.futures.ThreadPoolExecutor() as executor:
				futures = [executor.submit(worker, key, user_agent, proxy_type, proxy) for key in keys]
		except KeyboardInterrupt:
			os._exit(0)
	elif inp == 3:
		proxy_type = "socks5"
		try:
			with concurrent.futures.ThreadPoolExecutor() as executor:
				futures = [executor.submit(worker, key, user_agent, proxy_type, proxy) for key in keys]
		except KeyboardInterrupt:
			os._exit(0)
	else:
		print(f"Error, something is wrong.")

if __name__ == "__main__":
    main()
    
