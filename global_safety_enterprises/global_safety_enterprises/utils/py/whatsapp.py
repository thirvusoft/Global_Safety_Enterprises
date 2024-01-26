import frappe
from global_safety_enterprises.global_safety_enterprises.report.missed_follow_ups.missed_follow_ups import get_data as missed_follow_ups_get_data

from global_safety_enterprises.global_safety_enterprises.report.daily_follow_up_status.daily_follow_up_status import get_data as daily_follow_up_get_data

from frappe.utils import (
	add_days,
	nowdate,
    getdate,
    get_datetime,
    get_url_to_report,
    global_date_format,
    now,
    format_time
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
                # return False
    
            # else:
        
            #     return True

        except JSONDecodeError:
            frappe.log_error(title = "Not Sent Whatsapp", message = f"{response}")
            # return False

        except Exception as e:
            frappe.log_error(title = "Not Sent Whatsapp", message = f"{response}")
            # return False
        
        for report_name in ['Daily Follow Up Status','Missed Follow Ups']:
            if (report_name == 'Daily Follow Up Status' and ((daily_follow_quotation_count + daily_follow_lead_count) != 0)) or  (report_name == 'Missed Follow Ups' and ((today_missed_lead_follow_ups_count + today_missed_quotation_follow_ups_count) !=0 )):
                    if report_name == 'Daily Follow Up Status':
                        filters = {
                            "lead": 1,
                            "quotation": 1,
                            "from_date": add_days(nowdate(), -1),
                            "to_date": add_days(nowdate(), -1)
                        }
                    else:
                        filters = {
                            "lead": 1,
                            "quotation": 1,
                            "date": add_days(nowdate(), -1),
                        }
                    data_file = get_report_content(filters,report_name)
                    
                    pdf_name = report_name
            
                    urls = f'https://{frappe.local.site}{data_file.file_url}'

                    url_message = f"https://cloud.botsender.in/api/send.php?number=91{phone}&type=media&message={report_name}&media_url={urls}&filename={pdf_name}&instance_id=6500184CF31CC&access_token=298800d8ab85541dd846f73083c56be9"
                    
                    response = requests.request("GET", url_message, headers = {}, data = {})
                    try:
                        response = response.json()
                        if(response.get('status') == 'error'):
                            frappe.log_error(title = "Not Sent Whatsapp", message = f"{response}")
                            if report_name == 'Missed Follow Ups':
                                return False
                
                        else:
                            if report_name == 'Missed Follow Ups':
                                return True

                    except JSONDecodeError:
                        frappe.log_error(title = "Not Sent Whatsapp", message = f"{response}")
                        if report_name == 'Missed Follow Ups':
                            return False

                    except Exception as e:
                        frappe.log_error(title = "Not Sent Whatsapp", message = f"{response}")
                        if report_name == 'Missed Follow Ups':
                            return False


from frappe.utils.file_manager import save_file
from frappe.email.doctype.auto_email_report.auto_email_report import update_field_types,make_links
from frappe.utils.pdf import get_pdf
def get_report_content(filters,report_name):
    """Returns file in for the report in given format"""
    report = frappe.get_doc("Report", report_name)

    columns, data = report.get_data(
    user="Administrator",
    filters=filters,
    as_dict=True,
    ignore_prepared_report=True,
    are_default_filters=False,
    )

    # add serial numbers
    columns.insert(0, frappe._dict(fieldname="idx", label="", width="30px"))
    for i in range(len(data)):
        data[i]["idx"] = i + 1
    columns, data = make_links(columns, data)
    columns = update_field_types(columns)

    file_doc = save_file(nowdate(), get_pdf(get_html_table(columns,data,report_name),{"orientation": 'Landscape'} ),"Report", report_name)
    
    return file_doc
    
def get_html_table(columns=None, data=None,report_name=None):
    
    date_time = global_date_format(now()) + " " + format_time(now())
    report_doctype = frappe.db.get_value("Report", report_name, "ref_doctype")

    return frappe.render_template(
    "global_safety_enterprises/utils/html/auto_email_report.html",
    {
        "title": report_name,
        "description": '',
        "date_time": date_time,
        "columns": columns,
        "data": data,
        "report_url": get_url_to_report("Report", report_name, report_doctype),
        "report_name": report_name,
    },
    )