
__version__ = '0.0.1'
import erpnext, frappe
from erpnext.selling.doctype.quotation.quotation import set_expired_status
from global_safety_enterprises.global_safety_enterprises.utils.py.quotation import set_expired_status_global

def ses(*a, **b):
    if 'global_safety_enterprises' in frappe.get_installed_apps():
        return set_expired_status_global(*a, **b)
    return set_expired_status(*a, **b)

erpnext.selling.doctype.quotation.quotation.set_expired_status = ses
