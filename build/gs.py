import os
import utils
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def print_gradescope_classes(driver):
    # Turn the page source into a bs4 object for parsing
    bscontents = BeautifulSoup(driver.page_source, 'html.parser')

    # Get the name of the course, and print it out
    course_name_tag = bscontents.find('h1', class_='courseHeader--title')
    course_name = course_name_tag.text

    print("|", course_name)

    # Get all of the assignments for the class
    assignments = bscontents.find_all('tr', {'role': 'row'})

    # Gradescope in reverse order
    assignments.reverse()

    for assignment in assignments:
        # Check how much time is left for the assignment
        time_left = assignment.find('span',
                                    class_='submissionTimeChart--timeRemaining')
        if time_left is not None:
            due_date = time_left.text.lower() # Note: lowercase due_date
            cond = (("month" not in due_date) and ("week" not in due_date)
                    and ("year" not in due_date) and ("closes" not in due_date)
                    )
            if (cond):
                # Get the assignment name
                name_tag = assignment.find('th', {'role': 'rowheader'})
                name = name_tag.text

                # Print out the assignments name and due date
                print("  |", name, " is due:", due_date)
"""
Log in to gradescope and get all the assignments due within the 
next week
"""
def run_gradescope(username, password):
    # Create the chrome driver
    driver = webdriver.Chrome(os.path.dirname(__file__) + '/include/chromedriver')

    # Go to gradescope
    driver.get('https://gradescope.com')

    # Go to the school login for gradescope
    login_button = driver.find_element(By.CLASS_NAME, 'js-logInButton')
    login_button.click()
    school_crediential = driver.find_element(By.CLASS_NAME, 'tiiBtn--textWithIcon')
    school_crediential.click()

    # Go to calnet login
    school_logins = driver.find_elements(By.CLASS_NAME, 'samlProvider--name')
    for login in school_logins:
        if login.text == 'CalNet ID':
            print('found calnet. logging in')
            login.click()
            break

    # Log in to calnet
    utils.calnet_login(driver, username, password)

    # Wait for the duo log in by stalling
    utils.stall_forward(driver, "gradescope")
    print('Logged in to Gradescope, getting work needed to be done')

    # Note: find_element looks for 1st occurance, which is the most recent sem
    curr_class = driver.find_element(By.CLASS_NAME, 'courseList--coursesForTerm')
    class_boxes = curr_class.find_elements(By.CLASS_NAME, 'courseBox')

    # Note: Last class box is used for adding an additional class
    class_boxes_len = len(class_boxes) - 1

    used = 0 # How many of the classes have we seen (index in loop)

    while (used < class_boxes_len):
        # Go to the course website
        class_box = class_boxes[used]
        class_box.click()
        utils.stall_forward(driver, "courses")

        # Print the assignments due for this class
        print_gradescope_classes(driver)

        # Go back to main page
        driver.back()
        utils.stall_backward(driver, "courses")

        # reset variables
        used += 1
        curr_class = driver.find_element(By.CLASS_NAME,
                                         'courseList--coursesForTerm')
        class_boxes = curr_class.find_elements(By.CLASS_NAME, 'courseBox')


    driver.quit()

if __name__ == '__main__':

    usr = os.environ.get("username")
    pwd = os.environ.get("password")
    run_gradescope(usr, pwd)
