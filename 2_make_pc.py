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

file_path = 'created_tt.txt'
with open(file_path, 'r') as file:
    file_contents = file.read()

profile_names = ast.literal_eval(file_contents.split('=')[1].strip())

with open('model_database.json', 'r') as file:
    model_database = json.load(file)

"""if len(sys.argv) < 4:
    print("Usage: python script.py <record_id> <model_name> <num_profiles>")
    sys.exit(1)

record_id = sys.argv[1]
model_name = sys.argv[2]
num_profiles = int(sys.argv[3])"""

record_id = ''
model_name = 'Chloe'
num_profiles = int(1)

api_key = ''

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

API_BASE_URL = "http://localhost:3001/v1.0"

def close_profile(PROFILE_ID):
    stop_url = f"{API_BASE_URL}/browser_profiles/{PROFILE_ID}/stop"
    response = requests.get(stop_url, headers=headers)
    data = response.json()

    if not data.get('success'):
        print(f"Failed to close the Dolphin Anty profile {PROFILE_ID}.")
    else:
        print(f"Profile {PROFILE_ID} stopped successfully.")

def delete_profile(PROFILE_ID):
    print(f"Attempting to delete profile {PROFILE_ID}...")
    delete_url = f"https://dolphin-anty-api.com/browser_profiles/{PROFILE_ID}?forceDelete=1"
    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 200:
        print(f"Profile {PROFILE_ID} deleted successfully in Dolphin Anty")
    else:
        print(f"Failed to delete profile {PROFILE_ID} in Dolphin Anty. Status code: {response.status_code}")

def create_new_profile(model_name, headers):

    def fetch_profiles_with_tag(api_key, tag):
        url = "https://dolphin-anty-api.com/browser_profiles"
        params = {
            "query": tag,
            "limit": 50,
            "page": 1
        }
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            print(f"Failed to fetch profiles: {response.text}")
            return []

    def get_highest_profile_number(profiles, model_name):
        highest_number = 0
        for profile in profiles:
            name = profile.get('name', '')
            if name.startswith(model_name):
                try:
                    number = int(name.split()[-1])
                    highest_number = max(highest_number, number)
                except ValueError:
                    continue
        return highest_number

    def fetch_user_agent(headers):
        user_agent_url = "https://dolphin-anty-api.com/fingerprints/useragent"
        params = {
            "browser_type": "anty",
            "browser_version": "latest",
            "platform": platform
        }
        response = requests.get(user_agent_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get('data')
        else:
            return "Default User Agent String"

    def fetch_webgl_info():
        webgl_url = "https://dolphin-anty-api.com/fingerprints/fingerprint"
        params = {
            "platform": platform,
            "browser_type": "anty",
            "browser_version": "112",
            "type": "fingerprint",
            "screen": "2560x1440"
        }
        response = requests.get(webgl_url, headers=headers, params=params)
        if response.status_code == 200:
            response_data = response.json()

            unmasked_vendor = response_data.get('webgl', {}).get('unmaskedVendor', 'Default WebGL Vendor')
            unmasked_renderer = response_data.get('webgl', {}).get('unmaskedRenderer', 'Default WebGL Renderer')
            webgl2_maximum = json.loads(response_data.get('webgl2Maximum', '{}'))

            return unmasked_vendor, unmasked_renderer, webgl2_maximum
        else:
            return "Default WebGL Vendor", "Default WebGL Renderer", {}
        
    num_profiles = 1

    def read_proxies_from_file(file_path):
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file.readlines()]
        return proxies

    def rewrite_proxy_file(file_path, proxies):
        with open(file_path, 'w') as file:
            for proxy in proxies:
                file.write(proxy + '\n')

    proxy_file_path = r"G:\My Drive\Jays Bots\TikTok Bots\tiktok_proxies.txt"
    proxy_list = read_proxies_from_file(proxy_file_path)

    created_profiles = []

    for i in range(num_profiles):
        while True:
            platform = random.choice(['macos', 'windows'])
            profiles = fetch_profiles_with_tag(api_key, model_name)
            highest_number = get_highest_profile_number(profiles, model_name)
            new_profile_name = f"{model_name} {highest_number + 1}"

            new_user_agent = fetch_user_agent(headers)
            new_webgl_vendor, new_webgl_renderer, new_webgl2_maximum = fetch_webgl_info()

            random_proxy = random.choice(proxy_list)
            proxy_list.remove(random_proxy)
            rewrite_proxy_file(proxy_file_path, proxy_list)

            proxy_parts = random_proxy.split(':')
            proxy_host, proxy_port, proxy_login, proxy_password = proxy_parts

            proxy_config = {
                "type": "http",
                "host": proxy_host,
                "port": proxy_port,
                "login": proxy_login,
                "password": proxy_password,
                "name": "Sticky"
            }

            profile_data = {
                "name": new_profile_name,
                "tags": [model_name, "TikTok"],
                "tabs": [],
                "platform": platform,
                "mainWebsite": "", 
                "useragent": {
                    "mode": "manual",
                    "value": new_user_agent
                },
                "proxy": proxy_config,
                "webrtc": {
                    "mode": "altered"
                },
                "canvas": {
                    "mode": "noise"
                },
                "webgl": {
                    "mode": "noise"
                },
                "webglInfo": {
                    "mode": "manual",
                    "vendor": new_webgl_vendor if new_webgl_vendor else "Default WebGL Vendor",
                    "renderer": new_webgl_renderer if new_webgl_renderer else "Default WebGL Renderer",
                    "webgl2Maximum": new_webgl2_maximum if new_webgl2_maximum else "Default WebGL Renderer",
                },
                "timezone": {
                    "mode": "auto"
                },
                "locale": {
                    "mode": "auto"
                },
                "geolocation": {
                    "mode": "auto"
                },
                "cpu": {
                    "mode": "manual",
                    "value": random.choice([2, 4, 8, 16])
                },
                "memory": {
                    "mode": "manual",
                    "value": random.choice([4, 8, 16, 32])
                },
                "doNotTrack": 0,
                "browserType": "anty"
            }

            create_profile_url = "https://dolphin-anty-api.com/browser_profiles"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            try:
                create_response = requests.post(create_profile_url, headers=headers, data=json.dumps(profile_data))
                create_response.raise_for_status()
                create_response_data = create_response.json()
                if create_response_data.get("success") == 1:
                    browser_profile_id = create_response_data.get("browserProfileId", "Unknown ID")
                    print(f"Successfully created new profile '{new_profile_name}' with ID: {browser_profile_id}")
                    
                    created_profiles.append((new_profile_name, browser_profile_id))

                    
                    with open('created_profiles.txt', 'w') as file:
                        file.write("profile_names = {\n")
                        for name, id in created_profiles:
                            file.write(f"    '{id}': '{name}',\n")
                        file.write("}\n")
                        
                    return browser_profile_id

                else:
                    print(f"Failed to create new profile '{new_profile_name}': {create_response.text}")
                    return None

            except Exception as e:
                print(f"An error occurred while creating the profile '{new_profile_name}': {e}")
                return None

def send_to_discord(message):
    url = 'https://discord.com/api/webhooks/'  
    data = {
        'content': message,
        'username': 'Message Sender'
    }
    result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        pass

def get_today_date():
    tz = pytz.timezone('Europe/London') 
    today = datetime.now(tz).strftime('%Y-%m-%d')  
    return today

def find_or_create_today_record(today):
    records = airtable.get_all()  
    for record in records:
        record_date = record['fields'].get('Date', '')
        if record_date == today:
            return record['id'], record['fields']
    new_record = airtable.insert({'Date': today, 'Profiles Started': 0, 'Profiles That Made It Halfway': 0, 'Profiles That Finished': 0, 'Profiles Added To Airtable': 0})
    return new_record['id'], new_record['fields']

def update_profile_count(stage):
    today = get_today_date()
    record_id, fields = find_or_create_today_record(today)
    if stage == 'started':
        count = fields.get('Profiles Started', 0) + 1
        airtable.update(record_id, {'Profiles Started': count})
    elif stage == 'halfway':
        count = fields.get('Profiles That Made It Halfway', 0) + 1
        airtable.update(record_id, {'Profiles That Made It Halfway': count})
    elif stage == 'finished':
        count = fields.get('Profiles That Finished', 0) + 1
        airtable.update(record_id, {'Profiles That Finished': count})
    elif stage == 'added':
        count = fields.get('Profiles Added To Airtable', 0) + 1
        airtable.update(record_id, {'Profiles Added To Airtable': count})

def generate_usernames(surname):
    return [
        f"ashley{surname}x",
        f"ashley{surname}_x",
        f"ashley{surname}_",
        f"ashley_{surname}",
        f"ashley_{surname}x",
        f"ashley_{surname}_x",
        f"ashley_{surname}xx",
        f"ashleyx{surname}",
        f"ashleyx{surname}xo",
        f"ashleyx{surname}xx",
        f"ashleyx{surname}x_",
        f"ashleyx{surname}x",
        f"ashley{surname}xo",
        f"ashley{surname}x_",
        f"ashley{surname}1",
        f"ashley{surname}1x",
        f"ashley{surname}1_",
        f"ashley{surname}1_x",
        f"ashley{surname}0",
        f"ashley{surname}0_",
        f"ashley{surname}0x",
        f"ashley{surname}0_x",
    ]

def is_username_taken(username, driver, wait):
    username_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Username']")
    username_input.clear()
    username_input.send_keys(username)
    
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "p.css-1n8ha07-PInputError.e13yu7jj23")))
    
    username_status = driver.find_element(By.CSS_SELECTOR, "div.username-status").text
    return "Username is taken" in username_status
    
def start_profile(PROFILE_ID, attempt=1):
    try:
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
        
        chrome_driver_path = r"chromedriver.exe"
        service = Service(executable_path=chrome_driver_path)
        driver = uc.Chrome(service=service, options=options)

        driver.maximize_window()
        time.sleep(5)

        profile_name = profile_names.get(PROFILE_ID, f"Unknown Profile {PROFILE_ID}")

        wait = WebDriverWait(driver, 100)
        random_wait_time = random.uniform(3, 7)

        time.sleep(5)

        api_key_captcha = 'da3abd4887e4192f07778cde4270b58f'
        sadcaptcha = SeleniumSolver(driver, api_key_captcha)

        driver.get('https://accounts.google.com/signin')
        # update_profile_count('started')
        email = str(uuid.uuid4())
        password = email;
        email = email.replace('-', '.')[:15]
        randomInt = random.randint(1, 12)
        script_month = f"let month = document.getElementById('month'); month.value = {randomInt}"
        script_gender = f"let gender = document.getElementById('gender'); gender.value = 2"

        time.sleep(5)
        # First Part
        try:
            create_account = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Create account']]")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", create_account)
        except Exception as e: 
            error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            edit_message = f"@everyone {profile_name} failed clicking create_account button: {short_message}"
            send_to_discord(edit_message)
            print("------------------------------------------------------------------")
            raise Exception("Failed to interact with create_account button.")

        try:
            personal = wait.until(EC.presence_of_element_located((By.XPATH, "//li[.//span[text()='For my personal use']]")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", personal)
        except Exception as e: 
            error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            edit_message = f"@everyone {profile_name} failed clicking personal button: {short_message}"
            send_to_discord(edit_message)
            print("------------------------------------------------------------------")
            raise Exception("Failed to interact with personal button.")
        
        # Second Part
        try:
            name1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="firstName"]')))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", name1)
            name1.send_keys(model_name)            
        except Exception as e: 
            error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            edit_message = f"@everyone {profile_name} failed clicking name1 button: {short_message}"
            send_to_discord(edit_message)
            print("------------------------------------------------------------------")
            raise Exception("Failed to interact with name1 button.")
                                        
        try:
            namenext = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="collectNameNext"]/div/button')))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", namenext)
        except Exception as e: 
            error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            edit_message = f"@everyone {profile_name} failed clicking namenext button: {short_message}"
            send_to_discord(edit_message)
            print("------------------------------------------------------------------")
            raise Exception("Failed to interact with namenext button.")
        
        # Specific Data
        Utils.perform_action_raise_an_execption(driver, By.XPATH, '//*[@id="day"]', 'send_keys', random.randint(1, 28))
        Utils.perform_action_raise_an_execption(driver, By.XPATH, '//*[@id="month"]', 'execute_script', script_month)
        Utils.perform_action_raise_an_execption(driver, By.XPATH, '//*[@id="year"]', 'send_keys', random.randint(1990, 2000))
        Utils.perform_action_raise_an_execption(driver, By.XPATH, '//*[@id="gender"]', 'execute_script', script_gender)
        Utils.perform_action_raise_an_execption(driver, By.XPATH, '//*[@id="birthdaygenderNext"]/div/button', 'click')
        
        # Email Data
        try:
            time.sleep(3)
            create_gmail_option = driver.find_element(By.XPATH, "//div[contains(text(), 'Create your own Gmail address')]")
            time.sleep(1)
            driver.execute_script("arguments[0].click();", create_gmail_option)
        except Exception as e: 
            pass

        try:
            username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='Username' or @aria-label='Username']")))
            time.sleep(2)
            driver.execute_script("arguments[0].click();", username)
            username.send_keys(email)            
        except Exception as e: 
            error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            edit_message = f"@everyone {profile_name} failed clicking username button: {short_message}"
            send_to_discord(edit_message)
            print("------------------------------------------------------------------")
            raise Exception("Failed to interact with username button.")
                                    
        Utils.perform_action_raise_an_execption(driver, By.XPATH, '//*[@id="next"]/div/button', 'click')
        
        # Password Data
        Utils.perform_action_raise_an_execption(driver, By.XPATH, "//input[@aria-label='Password']", 'send_keys', password)
        Utils.perform_action_raise_an_execption(driver, By.XPATH, "//input[@aria-label='Confirm']", 'send_keys', password)
        Utils.perform_action_raise_an_execption(driver, By.XPATH, '//*[@id="createpasswordNext"]/div/button', 'click')

        time.sleep(10)

        order_response = SMS_SENDER.order_sms()
        if order_response["success"] == 1:
            order_id = order_response["order_id"]
            phone_number = order_response["number"]
            Utils.perform_action(driver, By.XPATH,'//*[@id="phoneNumberId"]', 'send_keys', phone_number)
            phone_confirm = driver.find_element(By.XPATH, "//button[.//span[text()='Next']]")
            phone_confirm.click()
            time.sleep(10)

            receive_sms = SMS_SENDER.check_sms(order_id); 
            print(receive_sms)
            Utils.perform_action_raise_an_execption(driver, By.XPATH, "//input[@id='code']", 'send_keys', receive_sms['sms'])
            Utils.perform_action_raise_an_execption(driver, By.XPATH, '//*[@id="next"]/div/button', 'click')
            Utils.perform_action_raise_an_execption(driver, By.XPATH, '//*[@id="recoverySkip"]/div/button', 'click')
            Utils.perform_action_raise_an_execption(driver, By.XPATH, '//*[@id="next"]/div/button', 'click')
            Utils.perform_action_raise_an_execption(driver, By.XPATH, "//div[@class='uxXgMe']//div[@role='radio' and contains(@class, 'zJKIV')]", 'click')
            Utils.perform_action_raise_an_execption(driver, By.XPATH, "//button[.//span[contains(text(), 'Next')]]", 'click')

            try:
                accept = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Accept all']]")))
                time.sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", accept)
                driver.execute_script("arguments[0].click();", accept)
            except Exception as e: 
                error_message = str(e)  
                short_message = '\n'.join(error_message.split('\n')[:3])
                edit_message = f"@everyone {profile_name} failed clicking accept button: {short_message}"
                send_to_discord(edit_message)
                print("------------------------------------------------------------------")
                raise Exception("Failed to interact with accept button.")
                            
            try:
                confirm = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Confirm']]")))
                time.sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", confirm)
                driver.execute_script("arguments[0].click();", confirm)
            except Exception as e: 
                error_message = str(e)  
                short_message = '\n'.join(error_message.split('\n')[:3])
                edit_message = f"@everyone {profile_name} failed clicking confirm button: {short_message}"
                send_to_discord(edit_message)
                print("------------------------------------------------------------------")
                raise Exception("Failed to interact with confirm button.")
            
            try:
                agree = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='I agree']]")))
                time.sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", agree)
                driver.execute_script("arguments[0].click();", agree)
            except Exception as e: 
                error_message = str(e)  
                short_message = '\n'.join(error_message.split('\n')[:3])
                edit_message = f"@everyone {profile_name} failed clicking agree button: {short_message}"
                send_to_discord(edit_message)
                print("------------------------------------------------------------------")
                raise Exception("Failed to interact with agree button.")

        time.sleep(25)

        driver.get('https://www.tiktok.com')

        login = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='header-login-button']")))
        time.sleep(1)
        driver.execute_script("arguments[0].click();", login)

        try:
            Utils.perform_action(driver, By.XPATH, "//div[contains(text(), 'Continue with Google')]", 'click')
            time.sleep(20)
            principle_page = driver.current_window_handle

            for window_handle in driver.window_handles:
                if window_handle != principle_page:
                    driver.switch_to.window(window_handle)
                    break

            Utils.perform_action(driver, By.XPATH, f"//div[@data-identifier='{email}@gmail.com']", 'click')
            Utils.perform_action(driver, By.XPATH, "//button[.//span[text()='Continue']]", 'click')
            driver.switch_to.window(principle_page)
        except Exception as e: 
            error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            edit_message = f"@everyone {profile_name} failed login into google: {short_message}"
            send_to_discord(edit_message)
            print("------------------------------------------------------------------")
            raise Exception("failed login into google.")
        
        time.sleep(10)
        
        sadcaptcha.solve_captcha_if_present()

        try:
            print("Try Month")
            month_dropdown_xpath = "//div[contains(@class, 'tiktok-1leicpq-DivSelectLabel') and text()='Month']"
            month_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, month_dropdown_xpath)))
            month_dropdown.click()

            random_month_index = random.randint(1, 12)

            random_month_xpath = f"//div[@id='Month-options-item-{random_month_index - 1}']"

            random_month = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, random_month_xpath)))
            random_month.click()

        except Exception as e: 
            """error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            edit_message = f"@everyone {profile_name} failed clicking month: {short_message}"
            send_to_discord(edit_message)
            print("------------------------------------------------------------------")
            raise Exception("failed clicking month.")"""
            pass
        
        try:
            print("Try Day")
            day_dropdown_xpath = "//div[contains(@class, 'tiktok-1leicpq-DivSelectLabel') and text()='Day']"
            day_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, day_dropdown_xpath)))
            day_dropdown.click()

            random_day_index = random.randint(1, 28)

            random_day_xpath = f"//div[@id='Day-options-item-{random_day_index - 1}']"

            random_day = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, random_day_xpath)))
            random_day.click()

        except Exception as e: 
            """error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            edit_message = f"@everyone {profile_name} failed clicking day: {short_message}"
            send_to_discord(edit_message)
            print("------------------------------------------------------------------")
            raise Exception("failed clicking day.")"""
            pass
        
        try:
            print("Try Year")
            year_dropdown_xpath = "//div[contains(@class, 'tiktok-1leicpq-DivSelectLabel') and text()='Year']"
            year_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, year_dropdown_xpath)))
            year_dropdown.click()

            random_year_index = random.randint(1995, 2002)

            base_year = 2000
            base_index = 23
            random_year_index_adjusted = base_index - (base_year - random_year_index)

            random_year_xpath = f"//div[@id='Year-options-item-{random_year_index_adjusted}']"

            random_year = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, random_year_xpath)))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", random_year)

        except Exception as e: 
            """error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            edit_message = f"@everyone {profile_name} failed clicking year: {short_message}"
            send_to_discord(edit_message)
            print("------------------------------------------------------------------")
            raise Exception("failed clicking year.")"""
            pass
        
        try:
            print("Try Next Login")
            next_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-e2e='next-button' and text()='Next']")))
            time.sleep(1)
            next_login.click()
        except Exception as e:
            pass

        """try:
            print("Try Gwg Again")
            try_gwg_again = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Continue with Google')]")))
            time.sleep(1)
            try_gwg_again.click()
        except Exception as e:
            pass"""

        Utils.perform_action_raise_an_execption(driver, By.XPATH, "//div[@class='tiktok-4y1w75-DivTextContainer e6sea5o0' and text()='Skip']", 'click')
        
        time.sleep(5)

        try:
            profile_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@data-e2e="nav-profile" and .//span[text()="Profile"]]')))
            time.sleep(random_wait_time)
            profile_link.click()
        except Exception as e: 
            pass

        try:
            edit_profile = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Edit profile']]")))
            time.sleep(random_wait_time)
            driver.execute_script("arguments[0].click();", edit_profile)
        except Exception as e: 
            error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            edit_message = f"@everyone {profile_name} failed clicking edit_profile button: {short_message}"
            send_to_discord(edit_message)
            print("------------------------------------------------------------------")
            raise Exception("Failed to interact with edit_profile button.")
        
        try:
            profile_pic = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'].css-4jv9vo-InputUpload.e13yu7jj22")))
            file_path = r'C:\Users\jayea\Documents\Python\VS Code\My Codes\Ashley Bot\ashleyPP.jpeg'  
            profile_pic.send_keys(file_path)
            time.sleep(random_wait_time)
        except Exception as e: 
            error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            profile_pic_message = f"@everyone {profile_name} failed clicking profile_pic button: {short_message}"
            send_to_discord(profile_pic_message)
            print("------------------------------------------------------------------")
            raise Exception("Failed to interact with profile_pic button.")

        file_path = r"G:\My Drive\Jays Bots\Dating Apps\Dating App General .txt Files\names.TXT"

        with open(file_path, 'r') as file:
            names = file.readlines()

        random_surname = random.choice(names).strip()
        full_name = f"Ashley Ivy"     

        try:
            name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Name'].css-18jpos7-InputText.e13yu7jj14")))
            time.sleep(random_wait_time)
            driver.execute_script("arguments[0].click();", name)
            name.send_keys(full_name)
        except Exception as e: 
            error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            name_message = f"@everyone {profile_name} failed clicking name button: {short_message}"
            send_to_discord(name_message)
            print("------------------------------------------------------------------")
            raise Exception("Failed to interact with name button.")
        
        try:
            usernames = generate_usernames(random_surname)
            for username in usernames:
                if not is_username_taken(username, driver, wait):
                    break
        except Exception as e: 
            error_message = str(e)  
            short_message = '\n'.join(error_message.split('\n')[:3])
            username_message = f"@everyone {profile_name} failed clicking username button: {short_message}"
            send_to_discord(username_message)
            print("------------------------------------------------------------------")
            raise Exception("Failed to interact with username button.")
        
        record_data = {
            "Email": email,
            "Password": password,
            "Model Name": model_name,
            "Username": username,
        }

        airtable.update(record_id, record_data) 
        #update_profile_count('added')

        close_profile(PROFILE_ID)
        if num_profiles == 1:
            sys.exit(0)

    except Exception as e:
        print(f"Exception encountered for profile {PROFILE_ID}: {e}. Attempting to retry...")
        if attempt <= 4:  
            print(f"Attempt {attempt}: Closing and deleting profile {PROFILE_ID}, then retrying...")
            close_profile(PROFILE_ID)
            delete_profile(PROFILE_ID)
            new_profile_id = create_new_profile(model_name, headers)  
            if new_profile_id:
                start_profile(new_profile_id, attempt+1)
            else:
                print(f"Failed to create a new profile on attempt {attempt}.")
        else:
            print(f"Failed to create profile after {attempt} attempts.")
            close_profile(PROFILE_ID)
            delete_profile(PROFILE_ID)    
            if num_profiles == 1:
                sys.exit(1)   

if model_name in model_database:
    attributes = model_database[model_name]

    with ThreadPoolExecutor(max_workers=15) as executor:
        list(executor.map(start_profile, profile_names))
else:
    print(f"Model named {model_name} not found!")
