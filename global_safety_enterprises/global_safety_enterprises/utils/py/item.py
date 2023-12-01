import frappe

from frappe.utils import (
    nowdate,
    add_days
)
def after_insert(self, event):

    create_item_price(self)

def validate(self, event):

    valuation_rate_validation(self)

    if not self.get("__islocal"):
        create_item_price(self)

def valuation_rate_validation(self):

    if self.valuation_rate <= 0:
        frappe.msgprint(msg = "Valuation Rate (Purchase Rate) Must Be Greater Than The <b>0</b>.", alert = True, indicator = "red", raise_exception = 1)

def create_item_price(self):

    default_price_list = frappe.db.get_single_value("Buying Settings", "buying_price_list")

    existing_matched_price_doc = frappe.db.exists("Item Price", {"item_code": self.name, "valid_from": nowdate(), "price_list": default_price_list})

    if existing_matched_price_doc:
        frappe.set_value("Item Price", existing_matched_price_doc, "price_list_rate", self.valuation_rate)

    else:

        existing_matched_price_doc = frappe.db.exists("Item Price", {"item_code": self.name, "price_list": default_price_list, "valid_upto": ("is", "not set")})
        
        if existing_matched_price_doc:
            frappe.set_value("Item Price", existing_matched_price_doc, "valid_upto", add_days(nowdate(), -1))

        new_doc = frappe.new_doc("Item Price")

        new_doc.item_code = self.name
        new_doc.price_list_rate = self.valuation_rate

        new_doc.price_list = default_price_list

        new_doc.save()