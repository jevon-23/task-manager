import os
import requests
import selenium
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# Get the username and password out the environment variables
username = os.environ.get("username")
password = os.environ.get("password")

"""
Store credential information in environment variable so 
that we do not have to store it in program.

Run this program from a .sh file that sets up environment vars,
but do not push that .sh file up to git
"""


"""
Log in to calnet. Calnet is the third party authenticator
for both gradescope and bcourses for berkeley students.

Input:
    driver: driver @ the calnet login page
"""
def calnet_login(driver):
    # Find the username and password field
    username_field = driver.find_element('id', 'username')
    password_field = driver.find_element('id', 'password')

    # Update the input fields
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Log in to calnet
    submit_button = driver.find_element('id', 'submit')
    submit_button.click()


def print_gradescope_classes(driver):
    # Turn the page source into a bs4 object for parsing
    bscontents = BeautifulSoup(driver.page_source, 'html.parser')

    # Get the name of the course, and print it out
    course_name_tag = bscontents.find('h1', class_='courseHeader--title')
    course_name = course_name_tag.text

    print("|", course_name)

    # Get all of the assignments for the class
    assignments = bscontents.find_all('tr', {'role': 'row'})
    assignments.reverse()

    for assignment in assignments:
        # Check how much time is left for the assignment
        time_left = assignment.find('span',
                                    class_='submissionTimeChart--timeRemaining')
        if time_left is not None:
            # NOTE: due date is in lower case
            due_date = time_left.text.lower()
            cond = (("month" not in due_date) and ("week" not in due_date)
                    and ("year" not in due_date) and ("closes" not in due_date)
                    )
            if (cond):

                # Get the assignment name
                name_tag = assignment.find('th', {'role': 'rowheader'})
                name = name_tag.text
                # print("name: ", name)

                # Print out the assignments name and due date
                print("  |", name, " is due:", due_date)
"""
Log in to gradescope and get all the assignments due within the 
next week
"""
def run_gradescope():
    # Go to gradescope
    driver = webdriver.Chrome('./chromedriver')
    driver.get('https://gradescope.com')

    # Go to the school login for gradescope
    login_button = driver.find_element(By.CLASS_NAME, 'js-logInButton')
    login_button.click()
    school_crediential = driver.find_element(By.CLASS_NAME, 'btnv7--textWithIcon')
    school_crediential.click()

    # Go to calnet login
    school_logins = driver.find_elements(By.CLASS_NAME, 'samlProvider--name')
    for login in school_logins:
        if login.text == 'CalNet ID':
            print('found calnet. logging in')
            login.click()
            break

    # Log in to calnet
    calnet_login(driver)

    print("Please accept duo request.")

    while ("trust" not in driver.page_source):
        continue

    # Hit the "do not trust" for the duo auth
    print("Not trusting the browser")
    no_trust = driver.find_element(By.ID, 'dont-trust-browser-button')
    no_trust.click()

    # Wait for the duo log in by stalling
    while ("gradescope" not in driver.current_url):
        continue

    print('Logged in to Gradescope, getting work needed to be done')

    # Note: find_element looks for 1st occurance, which is the most recent sem
    curr_class = driver.find_element(By.CLASS_NAME, 'courseList--coursesForTerm')
    class_boxes = curr_class.find_elements(By.CLASS_NAME, 'courseBox')

    # Note: Last class box is used for adding an additional class
    class_boxes_len = len(class_boxes) -1

    used = 0 # How many of the classes have we seen (index in loop)

    while (used < class_boxes_len):
        # Go to the course website
        class_box = class_boxes[used]
        class_box.click()
        while ("courses" not in driver.current_url):
            continue # stall

        # Print the assignments due for this class
        print_gradescope_classes(driver)

        # Go back to main page
        driver.back()
        while ("courses" in driver.current_url):
            continue # stall

        # reset variables
        used += 1
        curr_class = driver.find_element(By.CLASS_NAME,
                                         'courseList--coursesForTerm')
        class_boxes = curr_class.find_elements(By.CLASS_NAME, 'courseBox')


    driver.quit()

run_gradescope()

"""
Log in to bcourses and get all the assignments due within the 
next week
"""
def run_bcourses():
    driver = webdriver.Chrome('./include/chromedriver')
    driver.get('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fbcourses.berkeley.edu%2Flogin%2Fcas')

    calnet_login(driver)

    time.sleep(2)
    driver.quit()


# run_bcourses()

