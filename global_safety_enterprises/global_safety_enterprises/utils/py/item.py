import frappe

def after_insert(self, event):

    create_item_price(self)

def validate(self, event):

    valuation_rate_validation(self)

    # if not self.get("__islocal"):
    #     create_item_price(self)

def valuation_rate_validation(self):

    if self.valuation_rate <= 0:
        frappe.msgprint(msg = "Valuation Rate (Purchase Rate) Must Be Greater Than The <b>0</b>.", alert = True, indicator = "red", raise_exception = 1)

def create_item_price(self):

    new_doc = frappe.new_doc("Item Price")

    new_doc.item_code = self.name
    new_doc.price_list_rate = self.valuation_rate

    new_doc.price_list = frappe.db.get_single_value("Buying Settings", "buying_price_list")

    new_doc.save()
