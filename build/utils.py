from selenium.webdriver.common.by import By
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
def calnet_login(driver, username, password):
    # Find the username and password field
    username_field = driver.find_element('id', 'username')
    password_field = driver.find_element('id', 'password')

    # Update the input fields
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Log in to calnet
    submit_button = driver.find_element('id', 'submit')
    submit_button.click()

    print("Please accept duo request.")

    while ("trust" not in driver.page_source):
        continue

    # Hit the "do not trust" for the duo auth
    print("Not trusting the browser")
    no_trust = driver.find_element(By.ID, 'dont-trust-browser-button')
    no_trust.click()



"""
Put us into a blocked state until sub_string
is apart of our current url
"""
def stall_forward(driver, sub_string):
    while (sub_string not in driver.current_url):
        continue # stall

def stall_backward(driver, sub_string):
    while (sub_string in driver.current_url):
        continue # stall
