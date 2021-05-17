from termcolor import colored
from sys import version
print(colored(version,'magenta','on_yellow',attrs=['blink']))
print(colored(version,'cyan'))

from os import mkdir, name,environ
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep,time,ctime
from selenium.webdriver.common.keys import Keys
import datetime
from numpy import sign
from playsound import playsound
import pyttsx3
from selenium.webdriver.chrome.options import Options

path='/home/arash/Desktop/Link to ARASH/OTHER codes/Web Automata/WebAutomata github/geckodriver'
# driver = webdriver.Firefox(firefox_binary='/usr/bin/firefox')  #python
driver = webdriver.Firefox(executable_path=path)  #python
url = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
session_id = driver.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'
driver = webdriver.Remote(command_executor=url,desired_capabilities={})
driver.close()   # this prevents the dummy browser
driver.session_id = session_id
driver.get("http://www.mrsmart.in")