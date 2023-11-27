import frappe

def address_tax_validation(self,event):
    lead_list = self.links
    for i in lead_list:
        if i.link_doctype == 'Customer':
            cus_tax =frappe.get_doc('Customer',i.link_name)
            if not cus_tax =="In-State" and not self.state =="Tamil Nadu":
                form_link = frappe.get_desk_link('Customer', i.link_name)
                frappe.throw(f'State is not matched to the tax category of the {form_link}')

                

            

