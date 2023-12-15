app_name = "global_safety_enterprises"
app_title = "Global Safety Enterprises"
app_publisher = "Thirvusoft"
app_description = "CRM"
app_email = "thirvusoft@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/global_safety_enterprises/css/global_safety_enterprises.css"
app_include_js = "assets/global_safety_enterprises/js/desk.js"

# include js, css files in header of web template
# web_include_css = "/assets/global_safety_enterprises/css/global_safety_enterprises.css"
# web_include_js = "/assets/global_safety_enterprises/js/global_safety_enterprises.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "global_safety_enterprises/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Lead" : "/global_safety_enterprises/utils/js/lead.js",
            "Opportunity": "/global_safety_enterprises/utils/js/opportunity.js",
            "Customer": "/global_safety_enterprises/utils/js/customer.js",
            "Item": "/global_safety_enterprises/utils/js/item.js",
            "Quotation": "/global_safety_enterprises/utils/js/quotation.js",
            "User": "/global_safety_enterprises/utils/js/user.js",
			'Address': '/global_safety_enterprises/utils/js/address.js'
            }

doctype_list_js = {"Opportunity" : "/global_safety_enterprises/utils/js/opportunity_list.js",
                   "Lead": "/global_safety_enterprises/utils/js/lead_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "global_safety_enterprises/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
    "methods" : [
		"global_safety_enterprises.global_safety_enterprises.utils.py.quotation.tax_details",
    	"frappe.utils.data.money_in_words"
    ]
}

# Installation
# ------------

# before_install = "global_safety_enterprises.install.before_install"
# after_install = "global_safety_enterprises.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "global_safety_enterprises.uninstall.before_uninstall"
# after_uninstall = "global_safety_enterprises.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "global_safety_enterprises.utils.before_app_install"
# after_app_install = "global_safety_enterprises.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "global_safety_enterprises.utils.before_app_uninstall"
# after_app_uninstall = "global_safety_enterprises.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "global_safety_enterprises.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Lead": "global_safety_enterprises.global_safety_enterprises.utils.py.lead.CustomLead",
	'Opportunity':"global_safety_enterprises.global_safety_enterprises.utils.py.opportunity.CustomOpportunity",
	'Quotation':"global_safety_enterprises.global_safety_enterprises.utils.py.quotation.CustomQuotation"
}
override_doctype_dashboards = {
    "Lead": "global_safety_enterprises.global_safety_enterprises.utils.py.lead_dashboard.get_data",
}
# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Opportunity": {
		"validate": "global_safety_enterprises.global_safety_enterprises.utils.py.opportunity.validate"
	},
    "Quotation": {
		"validate": "global_safety_enterprises.global_safety_enterprises.utils.py.quotation.validate",
		'on_submit': "global_safety_enterprises.global_safety_enterprises.utils.py.quotation.update_ts_status",
        "on_change": "global_safety_enterprises.global_safety_enterprises.utils.py.quotation.on_update",
        "on_update_after_submit": "global_safety_enterprises.global_safety_enterprises.utils.py.quotation.validate_lost_status",
	},
	"Address": {
		"validate": "global_safety_enterprises.global_safety_enterprises.utils.py.address.address_tax_validation",
		'after_insert':"global_safety_enterprises.global_safety_enterprises.utils.py.address.after_save_address"
	},
	'Lead':{
		'validate':"global_safety_enterprises.global_safety_enterprises.utils.py.lead.validate"
	},
    
	"Item": {
        'validate': "global_safety_enterprises.global_safety_enterprises.utils.py.item.validate",
        'after_insert': "global_safety_enterprises.global_safety_enterprises.utils.py.item.after_insert"
	},
	'Contact':{
		'validate': "global_safety_enterprises.global_safety_enterprises.utils.py.contact.validate",
	},
    "User": {
        "validate":"global_safety_enterprises.global_safety_enterprises.utils.py.user.user_permission_create"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "all": [
        "global_safety_enterprises.global_safety_enterprises.utils.py.location.get_current_location"
	],
#	"daily": [
#		"global_safety_enterprises.tasks.daily"
#	],
#	"hourly": [
#		"global_safety_enterprises.tasks.hourly"
#	],
#	"weekly": [
#		"global_safety_enterprises.tasks.weekly"
#	],
#	"monthly": [
#		"global_safety_enterprises.tasks.monthly"
#	],
}

# Testing
# -------

# before_tests = "global_safety_enterprises.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "global_safety_enterprises.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "global_safety_enterprises.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["global_safety_enterprises.utils.before_request"]
# after_request = ["global_safety_enterprises.utils.after_request"]

# Job Events
# ----------
# before_job = ["global_safety_enterprises.utils.before_job"]
# after_job = ["global_safety_enterprises.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"global_safety_enterprises.auth.validate"
# ]
