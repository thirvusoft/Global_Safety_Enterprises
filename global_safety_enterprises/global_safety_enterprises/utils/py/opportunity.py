import frappe
from erpnext.setup.utils import get_exchange_rate
from frappe.model.mapper import get_mapped_doc
from erpnext.crm.doctype.opportunity.opportunity import Opportunity
from erpnext.crm.utils import (
    CRMNote,
    copy_comments,
    link_communications,
    link_open_events,
    link_open_tasks,
)
class CustomOpportunity(Opportunity):
    def after_insert(self):
        if self.opportunity_from == "Lead":
            # frappe.get_doc("Lead", self.party_name).set_status(update=True)

            link_open_tasks(self.opportunity_from, self.party_name, self)
            link_open_events(self.opportunity_from, self.party_name, self)
            if frappe.db.get_single_value("CRM Settings", "carry_forward_communication_and_comments"):
                copy_comments(self.opportunity_from, self.party_name, self)
                link_communications(self.opportunity_from, self.party_name, self)


def update_status(self,event):
    if self.party_name and self.opportunity_from == 'Lead':
        if self.status == 'Open':
            lead = frappe.get_doc('Lead',self.party_name)
            lead.db_set("status", 'Opportunity Open')
        elif self.status == 'Closed':
            lead = frappe.get_doc('Lead',self.party_name)
            lead.db_set("status", 'Opportunity Closed')

@frappe.whitelist()
def get_lead_addresses(lead_name):
    address=frappe.get_all(
            "Address",
            filters=[
            ["Dynamic Link", "link_doctype", "=", 'Lead'],
            ["Dynamic Link", "link_name", "=", lead_name],
            ["disabled", "=", 0],
            ],
            fields=['name','state']
        )
    if address:
        return address[0] 
    else:
        return address

@frappe.whitelist()

def create_customer(lead_name,customer,type,tax,opportunity_name,group = None):
	address=frappe.get_all(
			"Address",
			filters=[
			["Dynamic Link", "link_doctype", "=", 'Lead'],
			["Dynamic Link", "link_name", "=", lead_name],
			["disabled", "=", 0],
			],
			pluck="name",
		)
	contact=frappe.get_all(
		"Contact",
		filters=[
		["Dynamic Link", "link_doctype", "=", 'Lead'],
		["Dynamic Link", "link_name", "=", lead_name],
		],
		pluck="name",
	)

    cus_new =frappe.new_doc("Customer")
    cus_new.customer_name = customer
    cus_new.customer_type = type
    cus_new.customer_group = group
    cus_new.tax_category = tax
    cus_new.customer_primary_address = address[0] if address else ""
    cus_new.customer_primary_contact =contact[0] if contact else ""
    cus_new.opportunity_name = opportunity_name
    cus_new.lead_name = lead_name

    cus_new.save()
    return cus_new

@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
    def set_missing_values(source, target):
        from erpnext.controllers.accounts_controller import get_default_taxes_and_charges

        quotation = frappe.get_doc(target)

        company_currency = frappe.get_cached_value("Company", quotation.company, "default_currency")

        if company_currency == quotation.currency:
            exchange_rate = 1
        else:
            exchange_rate = get_exchange_rate(
                quotation.currency, company_currency, quotation.transaction_date, args="for_selling"
            )

        quotation.conversion_rate = exchange_rate

        # get default taxes
        taxes = get_default_taxes_and_charges(
            "Sales Taxes and Charges Template", company=quotation.company
        )
        if taxes.get("taxes"):
            quotation.update(taxes)

        quotation.run_method("set_missing_values")
        quotation.run_method("calculate_taxes_and_totals")
        if not source.get("items", []):
            quotation.opportunity = source.name

    doclist = get_mapped_doc(
        "Opportunity",
        source_name,
        {
            "Opportunity": {
                "doctype": "Quotation",
                "field_map": {"opportunity_from": "quotation_to", "name": "enq_no"},
            },
            "Opportunity Item": {
                "doctype": "Quotation Item",
                "field_map": {
                    "parent": "prevdoc_docname",
                    "parenttype": "prevdoc_doctype",
                    "uom": "stock_uom",
                },
                "add_if_empty": True,
            },
        },
        target_doc,
        set_missing_values,
    )
    
    customer_doc = frappe.get_doc("Customer", {"lead_name": doclist.party_name})
    
    doclist.quotation_to = "Customer"
    doclist.party_name = customer_doc.name
    doclist.tax_category = customer_doc.tax_category

    doclist.custom_quotation_owner = frappe.get_value("Opportunity", {"name": source_name}, "opportunity_owner")

    doclist.run_method("set_missing_values")

<<<<<<< HEAD
    return doclist
=======
	return doclist
>>>>>>> b859f93ad9efddebffed6d96b7a0f22f8eb6c00c
