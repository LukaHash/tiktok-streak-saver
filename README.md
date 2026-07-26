# TikTok Daily Auto-Messenger 📨

> A Python + Selenium script that automatically sends a message to every chat in TikTok Direct — **once per day**.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green.svg)](https://www.selenium.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📑 Table of Contents

- [About](#-about)
- [⚠️ Disclaimer](#️-disclaimer)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#%EF%B8%8F-configuration)
- [Usage](#%EF%B8%8F-usage)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [FAQ / Troubleshooting](#-faq--troubleshooting)
- [License](#-license)

---
### Script doesn't contain any proxies in code. so if you have troubles with connecting to TikTok it's only your problem :]


## 🎯 About



The script opens the **TikTok Messages** section, iterates through all available chats, and sends a predefined message to each one (default: `:]`).

To avoid spamming on every PC reboot, each successful run is recorded in a local **SQLite** database — the broadcast won't repeat within the same day. The script also waits for an active internet connection, which makes it perfect for adding to system startup.

---

## ⚠️ Disclaimer

**Using bots and automation violates TikTok's Terms of Service (ToS).**

- This may lead to a **temporary or permanent account ban**.
- Use this project **only on a test account** and **for educational purposes only**.
- The author is not responsible for any consequences resulting from the use of this code.

---

## ✨ Features

- ✅ Sends a message to **all** chats in a single pass
- ✅ Once-per-day protection against repeated runs (SQLite)
- ✅ Waits for an internet connection (up to 2 minutes) — handy for autostart
- ✅ Persistent Chrome profile keeps you logged in (sign in only once)
- ✅ Basic automation masking (`navigator.webdriver`, user-agent, automation flags disabled)
- ✅ Works from any directory (all paths are resolved relative to the script file)

---

## 🧰 Tech Stack

- **Python 3.8+**
- **Selenium** — browser automation
- **webdriver-manager** — automatic ChromeDriver downloads
- **SQLite3** — run tracking (bundled with Python)
- **Google Chrome** — the browser being automated

---

## 📋 Requirements

- **Python 3.8** or newer
- **Google Chrome** installed
- An active **TikTok** account
- Internet access

---

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/tiktok-daily-messenger.git
   cd tiktok-daily-messenger
   ```

2. (Recommended) Create a virtual environment:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

Open the script file and change the message if needed:

```python
# --- SETTINGS ---
MESSAGE_TO_SEND = ":]"   # ← Your message or emoji
```

**First run (authentication):**

1. Run the script.
2. In the Chrome window that opens, sign in to your TikTok account.
3. The session is stored in the `tiktok_profile/` folder — you won't need to log in again.

---

## ▶️ Usage

Standard run:

```bash
python main.py
```

**Autostart on PC boot (Windows):**

- Press `Win + R`, type `shell:startup`, and place a shortcut to the script there,
- or create a task in the **Windows Task Scheduler**.

The script waits for internet on its own and won't run the broadcast twice if it has already happened today.

---

## 🔍 How It Works

1. **Database check** — if today's broadcast has already run, the script exits immediately (no CPU/RAM wasted).
2. **Wait for internet** — tries to open a connection to `8.8.8.8:53` (up to 2 minutes).
3. **Launch the browser** — Chrome with the saved profile and stealth options.
4. **Send messages** — opens each chat one by one, types the text, and clicks "Send".
5. **Record the result** — on success, today's date is written to `TikTok_date.db`.

---

## 📁 Project Structure

```text
tiktok-daily-messenger/
├── main.py              # Main script
├── requirements.txt     # Project dependencies
├── README.md            # Documentation
├── TikTok_date.db       # Database of run dates (created automatically)
└── tiktok_profile/      # Chrome profile: cookies, session (created automatically)
```

---

## ❓ FAQ / Troubleshooting

**Chats don't appear / "session expired"**
Delete the `tiktok_profile/` folder and run the script again to log in.

**Message is not delivered in some chats**
TikTok periodically changes its markup. Check that the XPath selectors (`data-e2e` attributes) in the code are still up to date.

**I want to trigger the broadcast again on the same day**
Delete the `TikTok_date.db` file (or just today's row inside it) and run the script again.

**ChromeDriver / Chrome version error**
Update Google Chrome — `webdriver-manager` will pull a compatible driver on the next run.

---

## 📄 License

Distributed under the **MIT** License. See the [LICENSE](LICENSE) file for details.

---

*Built for educational purposes. Pull requests and issues are welcome 🙌*

---

### 📄 requirements.txt

```txt
selenium>=4.15.0
webdriver-manager>=4.0.0
```

> `os`, `sys`, `time`, `socket`, `sqlite3`, and `datetime` are part of Python's standard library, so they don't need to be listed in `requirements.txt`.


