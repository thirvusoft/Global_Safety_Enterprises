// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.query_reports["Missed Follow Ups"] = {
	"filters": [
		{
			fieldname: 'date',
			label: 'Date',
			fieldtype: 'Date',
			default: 'Today',
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
