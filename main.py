from time import sleep
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
load_dotenv('.env')

FACEBOOK_USERNAME = os.environ['EMAIL']
FACEBOOK_PASSWORD = os.environ['PASSWORD']

chrome_driver_path = os.environ['CHROME_DRIVER_PATH']
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get('https://tinder.com/')
# Sleep to add delay so that the new element has enough time to load.
sleep(5)

# Login to Tinder
login_button = driver.find_element(By.XPATH, '//*[@id="q554704800"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]')
login_button.click()
sleep(5)

# Login to Facebook
facebook_login = driver.find_element(By.XPATH, '//*[@id="q-1173676276"]/div/div/div[1]/div/div/div[3]/span/div[2]/button/span[2]')
facebook_login.click()
sleep(5)
# Switches to new Facebook window
facebook_login_window = driver.window_handles[1]
driver.switch_to.window(facebook_login_window)

# Fills the Facebook login form and log in
email = driver.find_element(By.XPATH, '//*[@id="email"]')
email.send_keys(FACEBOOK_USERNAME)
password = driver.find_element(By.XPATH, '//*[@id="pass"]')
password.send_keys(FACEBOOK_PASSWORD)
password.send_keys(Keys.ENTER)

# Switches back to Tinder
base_window = driver.window_handles[0]
driver.switch_to.window(base_window)
sleep(5)

# Allows Location and cookies pop-up, disallow notifications
allow_location_button = driver.find_element(By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
allow_location_button.click()
notifications_button = driver.find_element(By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
notifications_button.click()
cookies = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[1]/button')
cookies.click()

for n in range(100):
    sleep(2)
    try:
        # Clicks the like button
        like_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_button.click()

    # Clicks Back to Tinder after match popup
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, ".itsAMatch a")
            match_popup.click()

        # Adds delay if Like button is not reachable
        except NoSuchElementException:
            sleep(2)

driver.quit()