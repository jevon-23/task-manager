# task-manager
Scrapes gradescope and bcourses for what assignments are due within the next week

# Getting started

First thing you have to do is set up environment variables for credentials <br>
Use the credentials for the 3rd party authenticator to log in
<br>

```export username='{username}'```

<br>

```export password='{password}'```

<br>

Run program by running
<br>

```py ./build/main.py```

<br>

<br>
Under the hood, uses Selenium and BeautifulSoup to crawl both bcourses and gradescope for a given users credentials
<br> <br>
Will get the classes in Bcourses that are stored in the favorites, and the classes in gradescope under the most recent semester
<br><br>
Gets classes from gradescope that are in the most recent semester 
<br><br>

Will update readme with more info one I finish up and school slows down some for me, but not too much more than what is described here
<br><br>
# Enhancements
- Use cookies! 
- Could definetely speed up process if I can find a way to wait until the functionality of my loop is over before selenium begins to take next step
- Use only one driver instead of quitting!
- Make the selenium driver headless, and move through links instead of going through pages
  - Not sure if I can use this, depends on what gets loaded in the final page source I believe; look deeper into it
  
