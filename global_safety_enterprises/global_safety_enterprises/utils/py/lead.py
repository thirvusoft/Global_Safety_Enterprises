import frappe
from erpnext.crm.doctype.lead.lead import Lead
from frappe import _
def validate_replied(doc,event):
    if doc.status == 'Replied' and not doc.custom_view_follow_up_details_copy:
        frappe.msgprint('Minimum 1 row should be filled in Follow Up Table', raise_exception=1,indicator="red", title=_("Warning - Replied Status"))

    elif doc.status == 'Open' and doc.custom_view_follow_up_details_copy:
        doc.status = 'Replied'
        
class CustomLead(Lead):
    def before_insert(self):
        self.contact_doc = None
        if frappe.db.get_single_value("CRM Settings", "auto_creation_of_contact"):
            self.contact_doc = self.create_contact()
        if frappe.db.get_single_value("CRM Settings", "custom_auto_creation_of_address"):
            if self.custom_address_line and self.city and self.state:
                self.address_doc = self.create_address()

    def validate(self):
        self.set_full_name()
        self.set_lead_name()
        self.set_title()
        # self.set_status()
        self.check_email_id_is_unique()
        self.validate_email_id()

    def create_address(self):

        if not self.lead_name:
            self.set_full_name()
            self.set_lead_name()

        address = frappe.new_doc("Address")
        address.update(
            {   
                'address_title': self.first_name or self.lead_name,
                "address_line1": self.custom_address_line,
                "city": self.city,
                "state": self.state,
                "emaail_id": self.email_id,
                "phone": self.mobile_no,
            }
        )

        
        address.insert(ignore_permissions=True,ignore_mandatory= True)
        # contact.reload()  # load changes by hooks on contact

        return address

    def after_insert(self):
        self.link_to_contact()
        self.link_to_address()
    
    def link_to_address(self):
        if frappe.db.get_single_value("CRM Settings", "custom_auto_creation_of_address"):
            if self.custom_address_line and self.city and self.state:
                # update contact links
                if self.address_doc:
                    self.address_doc.append(
                        "links", {"link_doctype": "Lead", "link_name": self.name, "link_title": self.lead_name}
                    )
                    self.address_doc.save()
                if self.contact_doc:
                    self.contact_doc.address = self.address_doc.name
                    self.contact_doc.save()
            
    def create_contact(self):
        if not self.lead_name:
            self.set_full_name()
            self.set_lead_name()

        contact = frappe.new_doc("Contact")
        contact.update(
            {
                "first_name": self.first_name or self.lead_name,
                "last_name": self.last_name,
                "salutation": self.salutation,
                "gender": self.gender,
                "designation": self.custom_designation,
                'middle_name':self.middle_name,
                "company_name": self.company_name,
            }
        )

        if self.email_id:
            contact.append("email_ids", {"email_id": self.email_id, "is_primary": 1})

        if self.phone:
            contact.append("phone_nos", {"phone": self.phone, "is_primary_phone": 1})

        if self.mobile_no:
            contact.append("phone_nos", {"phone": self.mobile_no, "is_primary_mobile_no": 1})

        contact.insert(ignore_permissions=True)
        contact.reload()  # load changes by hooks on contact

        return contact
