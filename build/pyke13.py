import os
import utils
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time 
def run_pyke(cookies_file_path):

    email = os.environ.get("email")
    pwd = os.environ.get("pwd")

    # Create the chrome driver
    driver = webdriver.Chrome(os.path.dirname(__file__) + '/include/chromedriver')


    # Go to pyke
    driver.get('https://pike13.com/accounts/sign_in')

    # Find the email and pwd fields
    input_fields = driver.find_elements(By.TAG_NAME, 'input')
    e_field = [e for e in input_fields if e.get_attribute("type") == 'email'][0]
    p_field = [p for p in input_fields if p.get_attribute("type") == 'password'][0]

    e_field.send_keys(email)
    p_field.send_keys(pwd)

    # Find the submit button
    submit = driver.find_element(By.NAME, "button")
    submit.click()
    utils.stall_forward(driver, "tcs-")
    time.sleep(4)

    # Now we are on our pyke 13 schedule, get the sessions 4 this week
    events = driver.find_elements(By.CLASS_NAME, 'event_details')

    session_list = ["|Pyke 13"]
    for event in events:
        student = event.find_element(By.CLASS_NAME, 'clients')
        t = event.find_element(By.CLASS_NAME, 'time_range')

        out_str = "  | " + student.text + ' -> ' + t.text
        session_list.append(out_str)

    print("Finished reading pyke13 sessions")
    driver.quit()
    return session_list

if __name__ == '__main__':
    run_pyke("")
