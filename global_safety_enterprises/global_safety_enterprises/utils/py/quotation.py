import frappe
def update_status(self,event):
    if self.party_name and self.quotation_to == 'Customer':
        if frappe.get_value('Customer',self.customer,'lead_name'):
            lead = frappe.get_doc('Lead',frappe.get_value('Customer',self.customer,'lead_name'))
            lead.db_set("status", 'Quotation Created')
    if self.opportunity:
        opportunity = frappe.get_doc('Opportunity',self.opportunity)
        opportunity.db_set("status", 'Quotation Created')