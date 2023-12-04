import frappe
from global_safety_enterprises.global_safety_enterprises.utils.py.lead import validate_phone_number

def validate(self,event):
    validate_phone_number(self.mobile_no)
