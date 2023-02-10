#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: github.com/imvast
@Date: 2/5/2023
"""

import httpx
import os
import asyncio


class CapMonsterChecker:
    def __init__(self):
        with open("keys.txt", 'r') as f:
            self.keys = [line.strip() for line in f.readlines()]
    
    async def check_single_key(self, key):
        try:
            checkResp = await httpx.post(
                "https://api.capmonster.cloud/getBalance",
                json = { "clientKey": key }
            )
            if checkResp.status_code == 200:
                balance = checkResp.json().get('balance')
                if balance is not None:
                    print(f"[+] Valid Key: {key} | Balance: {balance}")
            elif checkResp.json().get('errorCode') == "ERROR_KEY_DOES_NOT_EXIST":
                print(f"[-] Invalid Key: {key}")
            else:
                print(f"[!] Error checking key: {key} | {checkResp.status_code} | {checkResp.json()}")
        except Exception as e:
            print(f"[ERROR] Exception in checker -> {e}")

    async def Check(self):
        print(f"[*] Starting checker with {len(self.keys)} keys...")
        tasks = [self.check_single_key(key) for key in self.keys]
        await asyncio.gather(*tasks)
                

if __name__ == "__main__":
    try:
        num_threads = int(input("Amount of Threads: "))
        asyncio.run(CapMonsterChecker().Check(), limit=num_threads)
    except KeyboardInterrupt:
        os._exit(0)
