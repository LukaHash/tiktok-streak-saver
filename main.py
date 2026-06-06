import os
import sys
import time
import socket
import sqlite3
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "TikTok_date.db")
profile_path = os.path.join(script_dir, "tiktok_profile")

# --- SETTINGS ---
MESSAGE_TO_SEND = ":]"


def is_already_run_today():
    """Check the database to see if the script has already run today."""
    today = str(date.today())
    conn = sqlite3.connect(db_path)
    crsr = conn.cursor()
    crsr.execute("""CREATE TABLE IF NOT EXISTS TikTok_date (date TEXT)""")
    crsr.execute("SELECT date FROM TikTok_date WHERE date = ?", (today,))
    row = crsr.fetchone()
    conn.close()
    return row is not None


def mark_as_run_today():
    """Save today's date to the database after a successful run."""
    today = str(date.today())
    conn = sqlite3.connect(db_path)
    crsr = conn.cursor()
    crsr.execute("INSERT INTO TikTok_date VALUES (?)", (today,))
    conn.commit()
    conn.close()
    print("[DB] Date saved. The script will not run again today.")


def wait_for_internet(timeout=120):
    """Wait for an active internet connection (up to 2 minutes)."""
    print("Checking internet connection...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            print("Internet connected!")
            return True
        except OSError:
            print("Waiting for internet connection...")
            time.sleep(5)
    print("Could not establish an internet connection. Exiting.")
    return False


def send_messages_workflow():
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={profile_path}")
    chrome_options.add_argument("--start-maximized")

    # Stealth options
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )

    try:
        print("Opening TikTok Messages...")
        driver.get("https://www.tiktok.com/messages?lang=en")

        print("Waiting for the page to load...")
        time.sleep(20)

        chat_selector = "//div[@data-e2e='dm-new-conversation-item']"

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, chat_selector))
            )
        except Exception:
            print("[Error] Chats did not appear. Session may have expired.")
            return False

        chats = driver.find_elements(By.XPATH, chat_selector)
        total_chats = len(chats)

        if total_chats == 0:
            print("[Error] Chat list is empty.")
            return False

        print(f"Chats found: {total_chats}. Starting broadcast...")

        for i in range(total_chats):
            try:
                chats = driver.find_elements(By.XPATH, chat_selector)
                if i >= len(chats):
                    break

                current_chat = chats[i]
                current_chat.click()
                print(f"[{i + 1}/{total_chats}] Chat opened")
                time.sleep(2.0)

                input_xpath = "//div[@contenteditable='true' and contains(@class, 'public-DraftEditor-content')]"
                input_box = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, input_xpath))
                )

                input_box.click()
                time.sleep(0.3)
                input_box.clear()
                input_box.send_keys(MESSAGE_TO_SEND)
                time.sleep(0.5)

                send_button_xpath = "//*[@data-e2e='dm-new-send-btn']"
                send_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, send_button_xpath))
                )

                send_button.click()
                print("-> Sent!")
                time.sleep(2.5)

            except Exception as e:
                print(f"[Skipped] Error in chat #{i + 1}: {e}")
                time.sleep(2.0)
                continue

        print("Broadcast completed successfully!")
        return True

    except Exception as general_error:
        print(f"Critical browser error: {general_error}")
        return False

    finally:
        driver.quit()


if __name__ == "__main__":
    if is_already_run_today():
        print("Today's broadcast has already been completed. Exiting.")
        sys.exit()

    if not wait_for_internet():
        sys.exit()

    success = send_messages_workflow()

    if success:
        mark_as_run_today()
    else:
        print("[Warning] Broadcast failed. Nothing written to DB. Will retry on next launch.")