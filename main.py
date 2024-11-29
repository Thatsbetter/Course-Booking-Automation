import time
import schedule  # Import the schedule library
from datetime import datetime,timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from credential import Credential
import pytz

def job(course_id):
    # Initialize the browser and perform all actions here
    with initialize_browser() as browser:
        browser.get("https://buchung.hochschulsport-hamburg.de/angebote/Wintersemester_2024_2025/_Volleyball.html")
        time.sleep(1)
        browser.find_element(By.NAME, course_id).click()
        try:
            cred = Credential()
            original_window = browser.current_window_handle
            window_handles = browser.window_handles

            for handle in window_handles:
                if handle != original_window:
                    browser.switch_to.window(handle)
                    break

            first_submit_button = browser.find_element(By.XPATH, '//input[@type="submit"]')
            browser.execute_script("arguments[0].scrollIntoView(true);", first_submit_button)
            first_submit_button.click()
            time.sleep(1)

            parent_element = browser.find_element(By.ID, "bs_pw_anm")
            browser.execute_script("arguments[0].classList.remove('hidden');", parent_element)

            element = browser.find_element(By.CSS_SELECTOR, ".bs_form_infotext")
            browser.execute_script("arguments[0].click();", element)

            parent_element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "bs_pw_anm"))
            )
            browser.execute_script("arguments[0].classList.remove('hidden');", parent_element)

            email_field = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div/div[2]/div[1]/div[2]/div[2]/input"))
            )

            email_field.send_keys(cred.get_username())

            password_field = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div/div[2]/div[1]/div[3]/div[2]/input"))
            )
            password_field.send_keys(cred.get_password())

            confirm_login = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "div.bs_form_foot:nth-child(5) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)"))
            )
            confirm_login.click()

            confirm_AGB = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div/div[3]/div[2]/label/input")))
            confirm_AGB.click()
            time.sleep(1)
            submit_form = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="bs_submit"]'))
            )
            submit_form.click()
            time.sleep(1)
            final_submit = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div/div[3]/div[1]/div[2]'))
            )
            final_submit.click()
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(2)

def initialize_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,700")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return browser

def determine_server_time_offset():
    """Determine the server's offset from UTC"""
    utc_now = datetime.utcnow()
    local_now = datetime.now()
    offset_seconds = (local_now - utc_now).total_seconds()

    return offset_seconds


def convert_to_server_time(berlin_hour, berlin_minute):
    """Convert given Berlin time to server's local time"""
    berlin_timezone = pytz.timezone('Europe/Berlin')
    berlin_time = datetime.now(berlin_timezone).replace(hour=berlin_hour, minute=berlin_minute, second=0, microsecond=0)
    utc_time = berlin_time.astimezone(pytz.utc)
    server_offset_seconds = determine_server_time_offset()
    server_time = utc_time + timedelta(seconds=server_offset_seconds)
    return server_time.time()



# Schedule the job for Thursdays at 21:01 local time
schedule.every().monday.at(convert_to_server_time(19, 31).strftime("%H:%M")).do(lambda:job("BS_Kursid_78053"))
schedule.every().thursday.at(convert_to_server_time(21,1).strftime("%H:%M")).do(lambda:job("BS_Kursid_79594"))

# Keep the script running
while True:
    schedule.run_pending()
    if (datetime.now().minute == 0):
        print(datetime.now())
    time.sleep(60)