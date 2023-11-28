import frappe
from frappe.utils import now_datetime

@frappe.whitelist()
def update_current_location(lat=None, long=None):
    if lat and long:
        frappe.db.set_value("User", frappe.session.user, "last_latitude", lat, update_modified=False)
        frappe.db.set_value("User", frappe.session.user, "last_longitude", long, update_modified=False)
        frappe.db.set_value("User", frappe.session.user, "last_location_updated_time", now_datetime(), update_modified=False)
        frappe.db.commit()

def get_current_location():
    frappe.publish_realtime("get_user_current_location")