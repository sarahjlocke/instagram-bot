from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time

# Get login credentials
USERNAME = input("Enter your Instagram username: ")
PASSWORD = input("Enter your Instagram password: ")

# Launch browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Go to login page
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)

# Accept cookies if shown
try:
    cookies = driver.find_element(By.XPATH, "//button[text()='Accept All']")
    cookies.click()
    time.sleep(2)
except:
    pass

# Log in
driver.find_element(By.NAME, "username").send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)
time.sleep(7)

# Skip save login
try:
    not_now = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
    not_now.click()
    time.sleep(3)
except:
    pass

# Go to profile
driver.get(f"https://www.instagram.com/{USERNAME}/")
time.sleep(5)

# --- FOLLOWING LIST ---
try:
    following_link = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "following"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", following_link)
    time.sleep(1)
    ActionChains(driver).move_to_element(following_link).click().perform()
    time.sleep(4)

    dialog = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
    )

    WebDriverWait(dialog, 20).until(
        EC.presence_of_element_located((By.XPATH, ".//a[contains(@href, '/')]"))
    )
    scroll_box = dialog

    for _ in range(100):  # SCROLL 100 TIMES FOR BIG ACCOUNTS
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(2)

    following_users = scroll_box.find_elements(By.XPATH, ".//a[contains(@href, '/')]")
    following = set(user.text for user in following_users if user.text)

    print(f"\n🧍 You're following {len(following)} accounts.")
    driver.find_element(By.XPATH, "//div[@role='dialog']//div/button").click()
    time.sleep(2)

except TimeoutException:
    print("❌ Timeout while loading following list.")
    following = set()

# --- FOLLOWERS LIST ---
try:
    followers_link = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "followers"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", followers_link)
    time.sleep(1)
    ActionChains(driver).move_to_element(followers_link).click().perform()
    time.sleep(4)

    dialog = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
    )

    WebDriverWait(dialog, 20).until(
        EC.presence_of_element_located((By.XPATH, ".//a[contains(@href, '/')]"))
    )
    scroll_box = dialog

    for _ in range(100):  # SCROLL 100 TIMES FOR BIG ACCOUNTS
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(2)

    followers_users = scroll_box.find_elements(By.XPATH, ".//a[contains(@href, '/')]")
    followers = set(user.text for user in followers_users if user.text)

    print(f"👀 You have {len(followers)} followers.")
    driver.find_element(By.XPATH, "//div[@role='dialog']//div/button").click()
    time.sleep(2)

except TimeoutException:
    print("❌ Timeout while loading followers list.")
    followers = set()

# --- COMPARE & REPORT ---
not_following_back = following - followers

print("\n🚨 These accounts don't follow you back:")
if not not_following_back:
    print("Everyone you follow follows you back! 🥹")
else:
    for user in sorted(not_following_back):
        print(" -", user)

# Close browser
driver.quit()