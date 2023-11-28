import frappe


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
def create_customer(lead_name,customer,type,tax,opportunity_name,group=None):
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
