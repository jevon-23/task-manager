import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils

def get_this_week():
    out = []
    today = datetime.date.today()

    this_week = [today + datetime.timedelta(days=i) for i in range(0, 8)]

    # Get in bcourses date format
    for date in this_week:
        day = date.day
        month_num = date.month

        # Convert month from number to shorthand name
        month_obj = datetime.datetime.strptime(str(month_num), "%m")
        month_name = month_obj.strftime("%b")

        # Put string in bcourses format:
        #   Jan 01
        date_string = month_name + ' ' + str(day)

        out.append(date_string)

    return out
def print_bcourses_classes(driver):

    # Try to go to the assignments tab
    try:
        # Find the assignment button
        assignment_button = driver.find_element(By.CLASS_NAME, 'assignments')
    except NoSuchElementException:
        print('No assignments for this class')
        return

    # click if available, and stall until we see the drop down menus
    assignment_button.click()
    utils.stall_forward(driver, "assignments")

    this_week = get_this_week()
    try:
        WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ig-header"))
        )
    except NoSuchElementException:
        print('could not load page in 10 seconds, or had an element exception')
        return


    # TODO: bcourses has a default pop up first, then the actual name of the tabs,
    #       so leave some time for it to load. (band-aid fix)
    time.sleep(2)

    # Find all of the assignments on the webpage
    assignments = driver.find_elements(By.CLASS_NAME, 'ig-info')
    for assignment in assignments:
        # Try to access the name through screen-reader tag
        try:
            name = assignment.find_element(By.CLASS_NAME, 'ig-title')
            due_date = assignment.find_element(By.CLASS_NAME, 'screenreader-only')
            # Find the assignment button
        except NoSuchElementException:
            print('could not find screen-reader')
            continue


        due_date_mo_day = ' '.join(due_date.text.split()[:2])

        if (due_date_mo_day in this_week):
            print('name: ', name.text, 'due date: ', due_date.text)

    time.sleep(5)

    # print('done')

    driver.back()
    utils.stall_backward(driver, "assignments")

"""
Log in to bcourses and get all the assignments due within the 
next week
"""
def run_bcourses(username, password):
    driver = webdriver.Chrome('./include/chromedriver')
    driver.get('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fbcourses.berkeley.edu%2Flogin%2Fcas')

    utils.calnet_login(driver, username, password)

    # Wait for the duo log in by stalling
    utils.stall_forward(driver, "bcourses")
    print('Logged in to Gradescope, getting work needed to be done')

    class_boxes = driver.find_elements(By.CLASS_NAME,
                                       'ic-DashboardCard__header_hero')
    class_boxes_len = len(class_boxes)

    used = 0 # How many of the classes have we seen (index in loop)
    while (used < class_boxes_len):
        # Go to the course website
        class_box = class_boxes[used]
        class_box.click()

        utils.stall_forward(driver, "courses")

        # Print the assignments due for this class
        print_bcourses_classes(driver)

        # Go back to main page
        driver.back()
        utils.stall_backward(driver, '/courses')

        # reset variables
        used += 1
        class_boxes = driver.find_elements(By.CLASS_NAME,
                                           'ic-DashboardCard__header_hero')

        # print('class_boxes: ', class_boxes)
    time.sleep(2)
    driver.quit()


if __name__ == '__main__':
    usr = os.environ.get("username")
    pwd = os.environ.get("password")
    run_bcourses(usr, pwd)
    # get_this_week()

