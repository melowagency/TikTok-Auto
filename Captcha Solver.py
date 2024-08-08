import ast
import sys
import json
import uuid
import pytz
import time
import random
import requests
from utils import Utils
from datetime import datetime
from airtable import Airtable
from selenium import webdriver
import undetected_chromedriver as uc
from SMS_Code.sms_sender import SMS_SENDER
from selenium.webdriver.common.by import By
from tiktok_captcha_solver import SeleniumSolver
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_key = ''
table_name = ''
airtable_api_key = ''

airtable = Airtable(base_key, table_name, airtable_api_key)

api_key = ''

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

API_BASE_URL = "http://localhost:3001/v1.0"

def start_profile(PROFILE_ID):
    start_url = f"{API_BASE_URL}/browser_profiles/{PROFILE_ID}/start?automation=1"
    response = requests.get(start_url)
    data = response.json()

    if not data.get('success'):
        raise Exception("Failed to start the Dolphin Anty profile.")

    port = data['automation']['port']
    options = webdriver.ChromeOptions()

    options.add_argument(f'--remote-debugging-port={port}')
    options.add_argument('--user-data-dir=./User_Data')
    
    debugger_address = f"localhost:{port}"
    options.debugger_address = debugger_address
    
    chrome_driver_path = r"C:\Users\jayea\Documents\Python\Apps\Real Chromedriver\Chromedriver 126\chromedriver-win64\chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    time.sleep(5)

    api_key_captcha = 'da3abd4887e4192f07778cde4270b58f'
    sadcaptcha = SeleniumSolver(driver, api_key_captcha)

    driver.get('https://www.tiktok.com')

    print("Waiting")
    time.sleep(120)

    print("Try Captcha")
    sadcaptcha.solve_captcha_if_present()

start_profile(434593955)



