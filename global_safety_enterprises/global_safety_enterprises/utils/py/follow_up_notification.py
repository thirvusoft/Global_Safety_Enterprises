import frappe
from frappe.integrations.doctype.slack_webhook_url.slack_webhook_url import send_slack_message
from frappe.utils import get_url_to_form

def follow_up_notification(doc, event=None):
    slack = frappe.db.get_value("Slack Webhook URL", {'name': ['like', '%notification%'], 'name': ['not like', '%alert%']}, 'name')
    if not slack:
        slack = frappe.db.get_value("Slack Webhook URL", {}, 'name')

    if slack:
        followup_table = "custom_view_follow_up_details_copy" if doc.get("doctype") == "Lead" else "custom_followup"
        p_doc = doc.get("_doc_before_save")
        
        if not p_doc:
            new_rows = doc.get(followup_table)
        else:
            exisiting_rows = [i.name for i in p_doc.get(followup_table)]
            new_rows = [i for i in doc.get(followup_table) if i.name not in exisiting_rows]
        
        if not new_rows:
            return
        
        message = f"""New Followup Update - <{get_url_to_form(doc.doctype, doc.name)}|{doc.doctype} {doc.name} - {doc.get("customer_name" if doc.doctype == 'Quotation' else "lead_name") or ''}>  \n"""

        for row in new_rows:
            message += f'''
*Date*: {row.get_formatted('date')}
*Followed By*: {row.get_formatted('followed_by')}
*Next Follow up Date*: {row.get_formatted('next_follow_up_date')}
*Next Follow up By*: {row.get_formatted('next_follow_up_by')}
*Mode of Communication*: {row.get_formatted('mode_of_communication')}
*Description*: {row.get_formatted('description')}
            \n'''
        
        send_slack_message(
            webhook_url=slack,
            message=message,
            reference_doctype=doc.doctype,
            reference_name=doc.name if doc.name else ''
        )
    
