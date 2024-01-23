import frappe
from global_safety_enterprises.global_safety_enterprises.report.missed_follow_ups.missed_follow_ups import get_data as missed_follow_ups_get_data

from global_safety_enterprises.global_safety_enterprises.report.daily_follow_up_status.daily_follow_up_status import get_data as daily_follow_up_get_data

from frappe.utils import (
	add_days,
	nowdate,
    getdate,
    get_datetime
)

from json.decoder import JSONDecodeError
import requests

def send_msg_whatsapp():
    
    filters = {
        "lead": 1,
        "date": add_days(nowdate(), -1),
    }
    
    today_missed_lead_follow_ups_count = len(missed_follow_ups_get_data(filters))
    
    filters = {
        "quotation": 1,
        "date": add_days(nowdate(), -1),
    }
    
    today_missed_quotation_follow_ups_count = len(missed_follow_ups_get_data(filters))
    
    filters = {
        "lead": 1,
        "from_date": add_days(nowdate(), -1),
        "to_date": add_days(nowdate(), -1)
    }
    
    daily_follow_lead_count = len(daily_follow_up_get_data(filters))
    
    filters = {
        "quotation": 1,
        "from_date": add_days(nowdate(), -1),
        "to_date": add_days(nowdate(), -1)
    }
    
    daily_follow_quotation_count = len(daily_follow_up_get_data(filters))
    
    phone_number_list = ["9488538080", "9840655558"]
    date = get_datetime(str(getdate(add_days(nowdate(), -1)))).strftime('%d-%m-%Y')
    msg = f"*About Follow-Ups Status For {date}:*%0A%0A"
    
    msg += f"*👉Lead Followed Count:* {daily_follow_lead_count}%0A"
    msg += f"*👉Quotation Followed Count:* {daily_follow_quotation_count}%0A"
    msg += f"*👉Lead Missed Follow-Up Count:* {today_missed_lead_follow_ups_count}%0A"
    msg += f"*👉Quotation Missed Follow-Up Count:* {today_missed_quotation_follow_ups_count}%0A"
    
    msg += "%0A By%0A Global Saftey Enterprises."
    
    for phone in phone_number_list:
    
        url_message = f"https://cloud.botsender.in/api/send.php?number=91{phone}&type=text&message={msg}&instance_id=6500184CF31CC&access_token=298800d8ab85541dd846f73083c56be9"
        
        response = requests.request("GET", url_message, headers = {}, data = {})

        try:
            response = response.json()
            
            if(response.get('status') == 'error'):
                frappe.log_error(title = "Not Sent Whatsapp", message = f"{response}")
                return False
    
            else:
        
                return True

        except JSONDecodeError:
            frappe.log_error(title = "Not Sent Whatsapp", message = f"{response}")
            return False

        except Exception as e:
            frappe.log_error(title = "Not Sent Whatsapp", message = f"{response}")
            return False