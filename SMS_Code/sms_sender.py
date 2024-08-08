import requests

class SMS_SENDER:
    
    _API_KEY = ""
    _SERVICE_NAME = 395
    _COUNTRY_CODE = 2
    _PRICING_OPTION = 0
    _ORDER_SMS_URL = "https://api.smspool.net/purchase/sms"
    _CHECK_SMS_URL = "https://api.smspool.net/sms/check"

    @staticmethod
    def order_sms():
        params = {
            "key": SMS_SENDER._API_KEY,
            "country": SMS_SENDER._COUNTRY_CODE,
            "service": SMS_SENDER._SERVICE_NAME,
            "pricing_option": SMS_SENDER._PRICING_OPTION
        }
        response = requests.post(SMS_SENDER._ORDER_SMS_URL, params=params)
        
        try:
            print(response.json())
            return response.json()
        except Exception as e:
            print("insufficient funds")
            return None
        
    @staticmethod
    def check_sms(order_id):
        params = {
            "key": SMS_SENDER._API_KEY,
            "orderid": order_id
        }
        response = requests.post(SMS_SENDER._CHECK_SMS_URL, params=params)
        try:
            return response.json()
        except Exception as e:
            print("Error decoding JSON response")
            print(e)
            return None




# TESTING COMAND
 
# result = SMS_SENDER.order_sms()
# print(result['success'])
# print(SMS_SENDER.check_sms("PCMOWTUP"))