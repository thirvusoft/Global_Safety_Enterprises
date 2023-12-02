import frappe

def address_tax_validation(self, event):

    lead_list = self.links

    for i in lead_list:

        if i.link_doctype == 'Customer':

            if self.state != "Tamil Nadu":
                frappe.set_value("Customer", i.link_name, "tax_category", "Out-State")
            
            else:
                frappe.set_value("Customer", i.link_name, "tax_category", "In-State")