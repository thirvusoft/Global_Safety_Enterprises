import frappe
def update_status(self,event):
    if self.party_name and self.opportunity_from == 'Lead':
        if self.status == 'Open':
            lead = frappe.get_doc('Lead',self.party_name)
            lead.db_set("status", 'Opportunity Created')
        elif self.status == 'Closed':
            lead = frappe.get_doc('Lead',self.party_name)
            lead.db_set("status", 'Opportunity Closed')
     
