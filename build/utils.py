from selenium.webdriver.common.by import By
import pickle
import threading

"""
Put us into a blocked state until sub_string
is apart of our current url
"""
def stall_forward(driver, sub_string):
    while (sub_string not in driver.current_url):
        continue # stall

"""
Put us into a blocked state until sub_string
is no longer apart of our current url
"""
def stall_backward(driver, sub_string):
    while (sub_string in driver.current_url):
        continue # stall
"""
Log in to calnet. Calnet is the third party authenticator
for both gradescope and bcourses for berkeley students.

Input:
    driver: driver @ the calnet login page
"""
def calnet_login(driver, username, password, cookies_file_path, calnet_lock):
    # cookies = pickle.load(open(cookies_file_path, "rb"))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    # Find the username and password field
    username_field = driver.find_element('id', 'username')
    password_field = driver.find_element('id', 'password')

    # Update the input fields
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Log in to calnet
    submit_button = driver.find_element('id', 'submit')

    
    # Block for the lock
    while calnet_lock.locked():
        continue

    # Lock, submit, release
    calnet_lock.acquire(blocking=True)
    submit_button.click()

    print("Please accept duo request.")
    while ("trust" not in driver.page_source):
        continue

    calnet_lock.release()

    # Hit the "do not trust" for the duo auth
    # print("Not trusting the browser")
    trust = driver.find_element(By.ID, 'trust-browser-button')

    # pickle.dump(driver.get_cookies(), open(cookies_file_path, "wb"))

    trust.click()


