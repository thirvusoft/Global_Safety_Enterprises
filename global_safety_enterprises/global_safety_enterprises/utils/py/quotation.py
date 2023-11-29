import frappe
from erpnext.selling.doctype.quotation.quotation import Quotation
def update_status(self,event):
    if self.party_name and self.quotation_to == 'Customer':
        if frappe.get_value('Customer',self.customer,'lead_name'):
            lead = frappe.get_doc('Lead',frappe.get_value('Customer',self.customer,'lead_name'))
            lead.db_set("status", 'Quotation Created')
    if self.opportunity:
        opportunity = frappe.get_doc('Opportunity',self.opportunity)
        opportunity.db_set("status", 'Quotation Created')


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

    def on_submit(self):
		# Check for Approving Authority
		frappe.get_doc("Authorization Control").validate_approving_authority(
			self.doctype, self.company, self.base_grand_total, self
		)

		# update enquiry status
		self.update_opportunity("Quotation")
		self.update_lead()
        self.status = self.custom_ts_status

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
