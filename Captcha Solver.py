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

base_key = 'appsPEs6eObqkIR17'
table_name = 'Profiles'
airtable_api_key = 'patdgvQXcMAwj7FOb.1feb4c60dc3475e1d70a576a5712003cb756f56eecf0d4105dfb992aee9f7af1'

airtable = Airtable(base_key, table_name, airtable_api_key)

api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZTYxOTRkMThkOGQzZGQyMTA0NTA4MTc2YWZlNjI5OTIzNzQ0OWZjMGRlNTNhMjA2YWFhZGE0Mzc3M2QxNGQ1MTg5NDkyZGQ2NzhkNDhkOWEiLCJpYXQiOjE3MDAzODY5MzkuMDc0MTU2LCJuYmYiOjE3MDAzODY5MzkuMDc0MTU4LCJleHAiOjE3MzE5MjI5MzkuMDY1MTE1LCJzdWIiOiIyNTg1Nzc1Iiwic2NvcGVzIjpbXX0.I571U2-XZl4HiRSAzO69RGUdsP5Wshrfz981T_gZ2ur_31r5NH9xIYy4_DkgJbSPlZ2bzr_yxius0CluLWy_uVLoZ4TEA0mTrnHRQgFvBrqpGWD1KvW36o5xYOLTKbC9l43xXcwMgr7NFlVSrfM-b2G0PijHsSsoAa_eUDf0GoKqTFq2a9MxiEYbWRzwb7Gie_H8Jj-ublthDA9r6jjKAQ1Y8af-7AygkZ9F-WnQEcgdhc-sZf-9H15xxyT5fCCksf7HIdp_TV2DF4lqwC20eTnneorz8jQ9W0PMiPTCLmYKl9Qntu9_5k7gj5zJfbaEfpaKQBa-Xmxzewi477p7xOCKqaPGoEQWWbP0SjI5YjLXBVLY09bqF059Hvs4AwYY4EWetOlSyHKKGzz0unrtFsLAchwO8S7HTARDuoYKLdOWApnnyHVUQTbxNKAdu5XYqLU3K3QcjsO1iJmGvoFXnmXginb5nZrEiDubruG3vuiuFoQTP_da7V8Zp5_Byymivdrbs5hePNqO2gtHLkeJYBvSQIOrJjxcUE8cg3DJpuiiUO_P56J0ABobXsZyMyHw259_yTa7zZi4_igYcv_A4LkGKgCa2_ic2RyvppR9AIGzygTJCrA2xIADiC6-SSAxyIoA8EWvoi7xCAhefMCESemrgbUPGkws8ktsah_z-0s'

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



