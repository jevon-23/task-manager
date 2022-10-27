import os
import gs # gradescope
import bc # bcourses

"""
To do list

Starts by grabbing the environment variables stored in:
    username = $username
    password = $password

These are supposed to be the username and password that is
used for 3rd party authentication being used for:
    - Gradescope
    - Bcourses

Then uses selinum to automate going through all of the courses
in both bcourses and gradescope, and prints out the assignments
that are due within the next week
"""
# Get the username and password out the environment variables
username = os.environ.get("username")
password = os.environ.get("password")

def main():
    # Get classes on gradescope
    gs.run_gradescope(username, password)
    
    # Get classes on bcourses
    bc.run_bcourses(username, password)

if __name__ == '__main__':
    main()
