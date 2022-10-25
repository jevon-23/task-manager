import os
import gs
import bc

# Get the username and password out the environment variables
username = os.environ.get("username")
password = os.environ.get("password")
def main():
    gs.run_gradescope(username, password)

if __name__ == '__main__':
    main()
