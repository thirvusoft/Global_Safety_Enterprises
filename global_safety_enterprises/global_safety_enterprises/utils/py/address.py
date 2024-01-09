import frappe
from global_safety_enterprises.global_safety_enterprises.utils.py.lead import validate_phone_number

def address_tax_validation(self, event):

    validate_phone_number(self.phone)

    lead_list = self.links

    for i in lead_list:

        if i.link_doctype == 'Customer':

            if self.state != "Tamil Nadu":
                frappe.db.set_value("Customer", i.link_name, "tax_category", "Out-State")
            
            else:
                frappe.db.set_value("Customer", i.link_name, "tax_category", "In-State")

def after_save_address(self,event):
    frappe.publish_realtime(
        "after_save_address"
    )