import threading
import sys
import os
import datetime
import keyboard
import tkinter as tk
from tkinter import *
import gs # gradescope
import bc # bcourses
import pyke13 # pyke
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
conig_filepath = './.work/config.txt'
username = os.environ.get("username")
password = os.environ.get("password")
output_file_path = './.work/task'
gs_cookies_file_path = './.work/gs_cookies.pkl'
bc_cookies_file_path = './.work/bc_cookies.pkl'

gs_assignments = []
bc_assignments = []
py_assignments = []

calnet_lock = threading.Lock()

def build_test_assignment():
    return ['abc', '123', 'abc123456']

# Get classes on gradescope
def thread_gs():
    global gs_assignments
    gs_assignments = gs.run_gradescope(username, password, gs_cookies_file_path, calnet_lock)

def thread_bc():
    global bc_assignments
    bc_assignments = bc.run_bcourses(username, password, bc_cookies_file_path, calnet_lock)

def thread_pyke():
    global py_assignments
    py_assignments = pyke13.run_pyke(email, pwd, "")

def build_assignment():

    gs_thread = threading.Thread(target=thread_gs, args=())
    bc_thread = threading.Thread(target=thread_bc, args=())
    py_thread = threading.Thread(target=thread_pyke, args=())

    gs_thread.start()
    bc_thread.start()
    py_thread.start()

    gs_thread.join()
    bc_thread.join()
    py_thread.join()

    assignments = gs_assignments + bc_assignments + py_assignments

    return assignments

def build_tk_window(assignment_str):

    root = Tk()
    # specify size of window.
    root.geometry("350x270")

    # Create text widget and specify size.
    T = Text(root, height = 40, width = 120)

    # Create label
    l = Label(root, text = "Homework due for the week")
    l.config(font =("Courier", 14))

    l.pack()
    T.pack()

    # Insert The Fact.
    T.insert(tk.END, assignment_str)
    return root

def process_args():
    assignment_str = " "
    if (len(sys.argv) == 1):
        assignments = build_assignment()
        # assignments = build_test_assignment()
        current_date = datetime.datetime.now().strftime("%x") + '\n'

        assignment_str = current_date + '\n'.join(assignments) + '\n'
    else:
        if (sys.argv[1] != 'print'):
            print("Invalid use of program: Fill in help later")
            exit(-1)
        assignment_str = open(output_file_path, "r").read()

    return assignment_str

def get_config():
    global username
    global password
    global email
    global pwd

    f = open(conig_filepath)
    txt = f.read()
    data = txt.split("\n")
    data = data[:len(data)-1]

    username = data[0]
    password = data[1]
    email = data[2]
    pwd = data[3]

def main():
    get_config()
    assignment_str = process_args()

    # Write the output to an output file
    with open(output_file_path, "w") as file:
        file.write(assignment_str)

    # Build the tkinter window 
    root = build_tk_window(assignment_str)

    # Key press actions for tkinter window
    def key_press_action(event):
        if (event.char == 'q'):
            root.destroy() # Quit


    root.bind('<KeyPress>', key_press_action)
    tk.mainloop()
if __name__ == '__main__':
    main()
