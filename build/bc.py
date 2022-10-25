import utils
import os
import requests
import selenium
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException



def print_bcourses_classes(driver):
    try:
        # Find the assignment button
        assignment_button = driver.find_element(By.CLASS_NAME, 'assignments')
    except NoSuchElementException:
        print('No assignments for this class')
        return
    
    assignment_button.click()
    utils.stall_forward(driver, "assignments")
    
    print('outta stall, driver.url: ', driver.current_url)
    bscontents = BeautifulSoup(driver.page_source, 'html.parser')

    assignments = bscontents.find_all('div',
                                  _class='ig-info')
    print('assignemts: ', assignments)
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
        print('used = ', used)
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

        print('class_boxes: ', class_boxes)
    time.sleep(2)
    driver.quit()


if __name__ == '__main__':
    usr = os.environ.get("username")
    pwd = os.environ.get("password")
    run_bcourses(usr, pwd)

