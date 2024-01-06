// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Follow Up Status"] = {
	"filters": [
		{
			fieldname: 'from_date',
			label: 'From Date',
			fieldtype: 'Date',
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: 'to_date',
			label: 'To Date',
			fieldtype: 'Date',
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: 'user',
			label: 'Follow Up By',
			fieldtype: 'Link',
			options: 'User'
		},
		{
			fieldname: 'lead',
			label: 'Lead',
			fieldtype: 'Check',
			default: 1
		},
		{
			fieldname: 'quotation',
			label: 'Quotation',
			fieldtype: 'Check',
			default: 1
		}
	]
};
