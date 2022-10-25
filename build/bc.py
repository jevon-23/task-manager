import utils
import os
import requests
import selenium
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By



"""
Log in to bcourses and get all the assignments due within the 
next week
"""
def run_bcourses(username, password):
    driver = webdriver.Chrome('./include/chromedriver')
    driver.get('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fbcourses.berkeley.edu%2Flogin%2Fcas')

    utils.calnet_login(driver, username, password)

    time.sleep(2)
    driver.quit()


if __name__ == '__main__':
    usr = os.environ.get("username")
    pwd = os.environ.get("password")
    run_bcourses(usr, pwd)

