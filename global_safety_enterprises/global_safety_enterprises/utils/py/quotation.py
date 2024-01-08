import frappe
from erpnext.selling.doctype.quotation.quotation import Quotation
from frappe.utils import getdate, nowdate
from global_safety_enterprises.global_safety_enterprises.utils.py.lead import validate_phone_number
from frappe.desk.reportview import get_filters_cond, get_match_cond

import json

def before_update_after_submit(doc, event=None):
    _action = doc._action
    doc._action = 'save'
    doc.run_before_save_methods()
    doc._action = _action
    doc.flags.ignore_validate_update_after_submit = True

def validate(self,event):
    update_status(self)
    validate_followup_date(self)
    update_date_status(self, event)
    validate_lost_status(self, event)
    validate_phone_number(self.custom_ts_contact_number)

def on_change(self, event):
    update_date_status(self, event)
    
def on_update(self, event):
         
    for row in reversed(self.custom_followup):
        
        if not row.longitude or not row.latitude:
                    
            frappe.publish_realtime("ts_get_user_current_location", row.name)
    
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
    if self.custom_followup and not self.custom_status_updated:
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

def tax_details(doc):

    sgst_list = []
    cgst_list = []
    igst_list = []

    for tax in doc.taxes:

        if "SGST" in tax.account_head and tax.tax_amount != 0:
            tax_details = json.loads(tax.item_wise_tax_detail)
            values = list(tax_details.values())

            for value in values:

                if sgst_list:

                    matched = False

                    for i in range (0, len(sgst_list), 1):

                        if value[0] != 0:

                            if sgst_list[i].get(f"SGST@ {value[0]} %"):
                                sgst_list[i][f"SGST@ {value[0]} %"] += value[1]
                                break

                            if len(sgst_list) == i + 1 and not matched:
                                sgst_list.append({f"SGST@ {value[0]} %": value[1]})
                else:
                    if value[0] != 0:
                        sgst_list.append({f"SGST@ {value[0]} %": value[1]})

        if "CGST" in tax.account_head and tax.tax_amount != 0:
            tax_details = json.loads(tax.item_wise_tax_detail)
            values = list(tax_details.values())

            for value in values:

                if cgst_list:

                    matched = False

                    for i in range (0, len(cgst_list), 1):

                        if value[0] != 0:

                            if cgst_list[i].get(f"CGST@ {value[0]} %"):
                                cgst_list[i][f"CGST@ {value[0]} %"] += value[1]
                                break

                            if len(cgst_list) == i + 1 and not matched:
                                cgst_list.append({f"CGST@ {value[0]} %": value[1]})
                else:
                    if value[0] != 0:
                        cgst_list.append({f"CGST@ {value[0]} %": value[1]})

        if "IGST" in tax.account_head and tax.tax_amount != 0:
            tax_details = json.loads(tax.item_wise_tax_detail)
            values = list(tax_details.values())

            for value in values:

                if igst_list:

                    matched = False

                    for i in range (0, len(igst_list), 1):

                        if value[0] != 0:

                            if igst_list[i].get(f"IGST@ {value[0]} %"):
                                igst_list[i][f"IGST@ {value[0]} %"] += value[1]
                                break

                            if len(igst_list) == i + 1 and not matched:
                                igst_list.append({f"IGST@ {value[0]} %": value[1]})
                else:
                    if value[0] != 0:
                        igst_list.append({f"IGST@ {value[0]} %": value[1]})

    key = []
    value = []

    if cgst_list and sgst_list:

        key.append("Taxable Value")
        value.append(f'{round(doc.net_total, 2): .2f}')

        for i in range(0, len(sgst_list), 1):
            key.append(list(sgst_list[i].keys())[0])
            
            final_value = f'{round(list(sgst_list[i].values())[0], 2): .2f}'
            value.append(final_value)


            key.append(list(cgst_list[i].keys())[0])

            final_value = f'{round(list(cgst_list[i].values())[0], 2): .2f}'
            value.append(final_value)

    elif igst_list:

        key.append("Taxable Value")
        value.append(f'{round(doc.net_total, 2): .2f}')

        for igst in igst_list:
            key.append(list(igst.keys())[0])

            final_value = f'{round(list(igst.values())[0], 2): .2f}'
            value.append(final_value)

    return key, value

# @frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
# def item_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
#     doctype = "Item"
#     conditions = []

#     if isinstance(filters, str):
#         filters = json.loads(filters)
#     parent_item_group = filters.get("parent_item_group")
#     parent_ig_cond = ""
#     if parent_item_group:
#         def get_child(item_group):
#             ig = frappe.get_all("Item Group", {"parent_item_group": item_group}, ["name", "is_group"])
#             res = [item_group]
#             for i in ig:
#                 if i.is_group:
#                     res += get_child(i.name)
#                 else:
#                     res.append(i.name)
#             return res
#         sub_groups = get_child(parent_item_group)
#         parent_ig_cond = f""" and `tabItem`.item_group in ('{"', '".join(sub_groups)}') """
#         del filters["parent_item_group"]
#     # Get searchfields from meta and use in Item Link field query
#     meta = frappe.get_meta(doctype, cached=True)
#     searchfields = meta.get_search_fields()

#     columns = ""
#     extra_searchfields = [field for field in searchfields if not field in ["name", "description"]]

#     if extra_searchfields:
#         columns += ", " + ", ".join(extra_searchfields)

#     if "description" in searchfields:
#         columns += """, if(length(tabItem.description) > 40, \
#             concat(substr(tabItem.description, 1, 40), "..."), description) as description"""

#     searchfields = searchfields + [
#         field
#         for field in [searchfield or "name", "item_code", "item_group", "item_name"]
#         if not field in searchfields
#     ]
#     searchfields = " or ".join([field + " like %(txt)s" for field in searchfields])

#     if filters and isinstance(filters, dict):
#         if filters.get("customer") or filters.get("supplier"):
#             party = filters.get("customer") or filters.get("supplier")
#             item_rules_list = frappe.get_all(
#                 "Party Specific Item", filters={"party": party}, fields=["restrict_based_on", "based_on_value"]
#             )

#             filters_dict = {}
#             for rule in item_rules_list:
#                 if rule["restrict_based_on"] == "Item":
#                     rule["restrict_based_on"] = "name"
#                 filters_dict[rule.restrict_based_on] = []

#             for rule in item_rules_list:
#                 filters_dict[rule.restrict_based_on].append(rule.based_on_value)

#             for filter in filters_dict:
#                 filters[frappe.scrub(filter)] = ["in", filters_dict[filter]]

#             if filters.get("customer"):
#                 del filters["customer"]
#             else:
#                 del filters["supplier"]
#         else:
#             filters.pop("customer", None)
#             filters.pop("supplier", None)

#     description_cond = ""
#     if frappe.db.count(doctype, cache=True) < 50000:
#         # scan description only if items are less than 50000
#         description_cond = "or tabItem.description LIKE %(txt)s"

#     return frappe.db.sql(
#         """select
#             tabItem.name {columns}
#         from tabItem
#         where tabItem.docstatus < 2
#             {parent_ig_cond}
#             and tabItem.disabled=0
#             and tabItem.has_variants=0
#             and (tabItem.end_of_life > %(today)s or ifnull(tabItem.end_of_life, '0000-00-00')='0000-00-00')
#             and ({scond} or tabItem.item_code IN (select parent from `tabItem Barcode` where barcode LIKE %(txt)s)
#                 {description_cond})
#             {fcond} {mcond}
#         order by
#             if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
#             if(locate(%(_txt)s, item_name), locate(%(_txt)s, item_name), 99999),
#             idx desc,
#             name, item_name
#         limit %(start)s, %(page_len)s """.format(
#             columns=columns,
#             scond=searchfields,
#             fcond=get_filters_cond(doctype, filters, conditions).replace("%", "%%"),
#             mcond=get_match_cond(doctype).replace("%", "%%"),
#             description_cond=description_cond,
#             parent_ig_cond=parent_ig_cond
#         ),
#         {
#             "today": nowdate(),
#             "txt": "%%%s%%" % txt,
#             "_txt": txt.replace("%", ""),
#             "start": start,
#             "page_len": page_len,
#         },
#         as_dict=as_dict,
#     )
    
    