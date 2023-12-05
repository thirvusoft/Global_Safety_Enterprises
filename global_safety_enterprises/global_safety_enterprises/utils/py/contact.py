import frappe
from global_safety_enterprises.global_safety_enterprises.utils.py.lead import validate_phone_number
from frappe.utils import comma_and,	get_link_to_form

def validate(self,event):
    validate_phone_number(self.mobile_no)
    validate_unique(self)

def validate_unique(self):
    for num in self.phone_nos:
        no = frappe.db.sql(f'''
            SELECT ph.phone, GROUP_CONCAT(r.link_name) AS reference_docs
            FROM `tabContact` as contact
            JOIN `tabDynamic Link` as r ON contact.name = r.parent
            Join `tabContact Phone` as ph on ph.parent = contact.name
            WHERE ph.phone = '{num.phone}' and r.link_doctype = 'Lead'

            GROUP BY ph.phone
            ''',as_dict=1)
        if no:
            docs = no[0].get('reference_docs').split(',')
            list_of_links = [get_link_to_form('Lead', p) for p in docs]
            frappe.msgprint(f'Mobile Number is already linked in Leads - {format(comma_and(list_of_links))}', title='Warning',indicator="orange",raise_exception=1)
