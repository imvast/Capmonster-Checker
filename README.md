# CapMonster Checker

![License](https://img.shields.io/github/license/Ggre55/Capmonster-Checker.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA)
![Stars](https://img.shields.io/github/stars/Ggre55/Capmonster-Checker.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA)
![Language](https://img.shields.io/github/languages/top/Ggre55/Capmonster-Checker.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python)


  <p align="center">
    <br />
    <br />
    <a href="https://t.me/Drwoop">🌌 Telegram</a>
    ·
    <a href="https://github.com/imvast/Capmonster-Checker#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/Ggre55/Capmonster-Checker/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/Ggre55/Capmonster-Checker/issues">💡 Request Feature</a>
  </p>
</div>


---------------------------------------

<p align="center">
  CapMonster Checker is a Python script that helps you manage and monitor multiple CapMonster API keys efficiently. It allows you to generate new keys, check their balance, and receive notifications on a Discord webhook. With added proxy support and error handling, this tool ensures smooth and reliable key checking. The script uses threading for faster processing and automatically removes invalid proxies. Stay informed with proper logging and take advantage of the latest bug fixes and improvements. Simplify your CapMonster key management with this user-friendly checker tool.

</p>

---------------------------------------

### ⚙️ Installation
> Checker:
* Requires: `Python 3.10+`, `colorama`, `httpx`, `json`
* Start: `main.py`

---------------------------------------

### 🔥 Features
* User Friendly Interface
* Fast Speeds
* Simple & Easy Setup
* Support proxy
* Better error Handling
* Remove Invalid Proxies
* Threading or Asynchronous Requests


---------------------------------------

### 🚀 Milestones
* 10 Stars - Better Error Handling [`DONE`]
* suggest more things for me to do cuz idk 

---------------------------------------

### ❗ Disclaimers
- I am not responsible for anything that may happen, such as, API Blocking, Account Termination, etc.
- This **may** slow down your wifi and/or host computer
- This was a quick project that was made for fun, so if you want to see further updates, star the repo & create an "issue" [here](https://github.com/Ggre55/Capmonster-Checker/issues)

---------------------------------------

### ❗ CREDIT
idea from ! Otex ~ discord.gg/otex
pulled from ! [Imvast](https://github.com/imvast/Capmonster-Checker) 

---------------------------------------
### 📜 ChangeLog

## v0.0.1 (2/6/2023)
- Initial Release ❤️

## v0.2.1 (4/8/2023)
- Updated, bug fixes ❤️
- Added proxy support:
  Now, if there's a file named `proxies.txt` in the same folder as the script, the script will load the proxies from that file. If the user chooses to use proxies, it will randomly select one from the list of loaded proxies for each HTTP request. If the user decides not to use proxies, the script will make the HTTP requests without using any proxies.
- Better error handling ❤️
- Random Proxy Selection:
  Instead of randomly selecting a proxy for each key check, we'll choose a single proxy and use it for multiple key checks before changing to another one. This will reduce the overhead of changing proxies frequently.
- Threading or Asynchronous Requests:
  Using Python's `concurrent.futures` module to check multiple keys simultaneously with threading.
- Remove Invalid Proxies:
  We implement a function to check the validity of proxies before using them for HTTP requests. If a proxy is found to be invalid, it will be removed from the proxy pool.
- Logging:
  We'll add proper logging to log the results, errors, and status of key checks and other operations.

---------------------------------------

