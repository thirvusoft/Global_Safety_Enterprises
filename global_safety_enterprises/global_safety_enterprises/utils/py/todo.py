import frappe

def validate(doc, action):
    next_follow_up_date = None
    follow_ups = doc.custom_follow_ups
    if follow_ups:
        last_follow_up = follow_ups[-1] 
        next_follow_up_date = last_follow_up.get('next_follow_up_date')
    if next_follow_up_date:
        doc.date = next_follow_up_date