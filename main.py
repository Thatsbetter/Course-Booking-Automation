import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


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


with initialize_browser() as browser:
    browser.get("https://buchung.hochschulsport-hamburg.de/angebote/Sommersemester_2024/_Beachvolleyball.html")
    time.sleep(1)
    browser.find_element(By.NAME, 'BS_Kursid_77860').click()
    time.sleep(1)
    try:
        # Get the current window handles
        original_window = browser.current_window_handle
        window_handles = browser.window_handles

        # Switch to the new tab
        for handle in window_handles:
            if handle != original_window:
                browser.switch_to.window(handle)
                break
        # Perform actions in the new tab
        first_submit_button = browser.find_element(By.XPATH, '//input[@type="submit"]')
        browser.execute_script("arguments[0].scrollIntoView(true);", first_submit_button)
        first_submit_button.click()
        time.sleep(1)
        # Locate the element
        ###########################

        parent_element = browser.find_element(By.ID, "bs_pw_anm")
        browser.execute_script("arguments[0].classList.remove('hidden');", parent_element)

        # Locate the target element after making it visible
        element = browser.find_element(By.CSS_SELECTOR, ".bs_form_infotext")

        # Execute JavaScript to click on the element
        browser.execute_script("arguments[0].click();", element)

        ###########################

        # Wait for the parent element to be present and then remove the 'hidden' class
        parent_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "bs_pw_anm"))
        )
        browser.execute_script("arguments[0].classList.remove('hidden');", parent_element)

        # Input "username" into the email field using its custom attribute
        email_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div/div[2]/div[1]/div[2]/div[2]/input"))
        )
        email_field.send_keys("XXX")

        # Input "user" into the password field using its custom attribute
        password_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div/div[2]/div[1]/div[3]/div[2]/input"))
        )
        password_field.send_keys("XXX")

        confirm_login = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "div.bs_form_foot:nth-child(5) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)"))
        )
        confirm_login.click()

        ##################
        confirm_AGB = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div/div[3]/div[2]/label/input")))
        confirm_AGB.click()

        final_submit = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="bs_submit"]'))
        )
        final_submit.click()

    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(10)  # Optional: Wait for 5 seconds before closing the browser
