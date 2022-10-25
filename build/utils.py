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
