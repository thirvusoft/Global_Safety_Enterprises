import frappe

def after_insert(self, event):

    create_item_price(self)

def validate(self, event):

    if not self.get("__islocal"):
        create_item_price(self)

def create_item_price(self):

    new_doc = frappe.new_doc("Item Price")

    new_doc.item_code = self.name
    new_doc.price_list_rate = self.valuation_rate

    new_doc.price_list = frappe.db.get_single_value("Buying Settings", "buying_price_list")

    new_doc.save()
