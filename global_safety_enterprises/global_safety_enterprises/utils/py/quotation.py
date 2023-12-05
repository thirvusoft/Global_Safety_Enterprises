import frappe
from erpnext.selling.doctype.quotation.quotation import Quotation
from frappe.utils import getdate, nowdate
from global_safety_enterprises.global_safety_enterprises.utils.py.lead import validate_phone_number

def validate(self,event):
    update_status(self)
    validate_followup_date(self)
    update_date_status(self, event)
    validate_lost_status(self, event)
    validate_phone_number(self.custom_ts_contact_number)
    
def on_update(self, event):
    update_date_status(self, event)
    
def validate_followup_date(self):
    for date in self.custom_followup:
        for other in range(date.idx,len(self.custom_followup),1):
            if getdate(date.date) > getdate(self.custom_followup[other].date):
                frappe.msgprint(f'The Date in <span style="color:red">Row - {self.custom_followup[other].idx}</span> is earlier than the Date in <span style="color:red">Row - {date.idx}</span>. Please review the Date ..',title='Warning',raise_exception = 1)

def update_status(self):
    if self.party_name and self.quotation_to == 'Customer':
        if frappe.get_value('Customer',self.customer,'lead_name'):
            lead = frappe.get_doc('Lead',frappe.get_value('Customer',self.customer,'lead_name'))
            lead.db_set("status", 'Quotation Created')
    if self.opportunity:
        opportunity = frappe.get_doc('Opportunity',self.opportunity)
        opportunity.db_set("status", 'Quotation Created')
        
def validate_lost_status(self, event):
    if self.custom_followup:
        if self.custom_followup[-1].status == "Do Not Disturb" :
            if self.docstatus == 1:
                self.db_set('status' , "Lost")
                self.reload()
            if self.docstatus == 0:
                frappe.throw("Kindly Submit This Quotation and then update the status")

def update_ts_status(doc,event):
    doc.db_set('status',doc.custom_ts_status)

def update_date_status(self, event):
    if self.status == "Ordered" and event == "validate":
        self.custom_ts_orderd_date = nowdate()

    elif self.status == "Lost" and event == "validate":
        self.custom_ts_lost_date = nowdate()

    elif self.status == "Ordered" and event == "on_change":
        self.custom_ts_orderd_date = nowdate()
        self.db_update()

    elif self.status == "Lost" and event == "on_change":
        self.custom_ts_lost_date = nowdate()
        self.db_update()

class CustomQuotation(Quotation):
    def on_cancel(self):
        if self.lost_reasons:
            self.lost_reasons = []
        super(Quotation, self).on_cancel()

        # update enquiry status
        # self.set_status(update=True)
        self.status = 'Cancelled'
        self.update_opportunity("Open")
        self.update_lead()

    def validate(self):
        super(Quotation, self).validate()
        # self.set_status()
        self.validate_uom_is_integer("stock_uom", "qty")
        self.validate_valid_till()
        self.set_customer_name()
        if self.items:
            self.with_items = 1

        from erpnext.stock.doctype.packed_item.packed_item import make_packing_list

        make_packing_list(self)
    
    def update_opportunity_status(self, status, opportunity=None):
        if not opportunity:
            opportunity = self.opportunity

        opp = frappe.get_doc("Opportunity", opportunity)
        # opp.set_status(status=status, update=True)
    
    def update_lead(self):
        if self.quotation_to == "Lead" and self.party_name:
            pass
            # frappe.get_doc("Lead", self.party_name).set_status(update=True)
