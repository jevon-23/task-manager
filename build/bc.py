import os
import time
import datetime
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils

"""Gets the next 8 days including today (ex: Mon->Mon)"""
def get_this_week():
    # A of strings representing this week
    this_week = []

    today = datetime.date.today()
    # The next 7 days
    week = [today + datetime.timedelta(days=i) for i in range(0, 8)]

    # Get in bcourses date format
    for date in week:
        day = date.day
        month_num = date.month

        # Convert month from number to shorthand name
        month_obj = datetime.datetime.strptime(str(month_num), "%m")
        month_name = month_obj.strftime("%b")

        # Put string in bcourses format:
        #   Jan 01
        date_string = month_name + ' ' + str(day)

        this_week.append(date_string)
    return this_week

"""Prints all of the assignments due within the next week
that are on the bcourses starred page. 

Input:
    driver: Webdriver elemement already at the course webpage in bcourses
"""
def print_bcourses_classes(driver):

    # Try to go to the assignments tab
    try:
        # Find the assignment button
        assignment_button = driver.find_element(By.CLASS_NAME, 'assignments')
    except NoSuchElementException:
        # No assignments for this class
        return []

    # click if available, and stall until we see the drop down menus
    assignment_button.click()
    utils.stall_forward(driver, "assignments")

    # Get the next seven days
    this_week = get_this_week()

    # Wait for the right header to load on the page before continuing
    try:
        WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ig-header"))
        )
    except NoSuchElementException:
        print('could not load page in 10 seconds, or had an element exception')
        return []


    # TODO: bcourses has a default pop up first, then the actual name of the tabs,
    #       so leave some time for it to load. (band-aid fix)
    time.sleep(2)

    assignment_list = [] # output list 

    course_name = driver.find_elements(By.CLASS_NAME, 'ellipsible')[1].text
    course_name_str = "| " + course_name
    assignment_list.append(course_name_str)

    # Find all of the assignments on the webpage
    assignments = driver.find_elements(By.CLASS_NAME, 'ig-info')
    for assignment in assignments:
        # Try to access the name through screen-reader tag
        try:
            name = assignment.find_element(By.CLASS_NAME, 'ig-title')
            due_date = assignment.find_element(By.CLASS_NAME, 'screenreader-only')
            # Find the assignment button
        except NoSuchElementException:
            # could not find ig-title or screen-reader
            continue


        # First two words of due date is the month and day
        due_date_mo_day = ' '.join(due_date.text.split()[:2])

        if (due_date_mo_day in this_week):
            assignment_str = "  | " + name.text +  " is due: " + due_date.text
            assignment_list.append(assignment_str)

    time.sleep(5) # Give it some time to finish
    driver.back()
    utils.stall_backward(driver, "assignments")
    return assignment_list

"""
Log in to bcourses and get all the assignments due within the 
next week
"""
def run_bcourses(username, password, cookies_file_path):

    assignment_list = []
    driver = webdriver.Chrome(os.path.dirname(__file__) + '/include/chromedriver')
    driver.get('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fbcourses.berkeley.edu%2Flogin%2Fcas')

    # Add the cookies to the driver 
    # cookies = pickle.load(open(cookies_file_path, "rb"))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    utils.calnet_login(driver, username, password, cookies_file_path)
    utils.stall_forward(driver, "bcourses")

    pickle.dump(driver.get_cookies(), open(cookies_file_path, "wb"))
    
    print('Logged in to Bcourses, getting work needed to be done')

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
        assignment_list += print_bcourses_classes(driver)

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


    return assignment_list


if __name__ == '__main__':
    usr = os.environ.get("username")
    pwd = os.environ.get("password")
    run_bcourses(usr, pwd)

