# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe

def execute(filters = None):

	columns = get_columns(filters)

	data = get_data(filters)

	return columns, data

def get_columns(filters):

	columns = [

		{
			'fieldname': 'lead_quotation_id',
			'fieldtype': 'Data',
			'label': 'Lead / Quotation ID',
			'width': 182
		},

		{
			'fieldname': 'lead_name',
			'fieldtype': 'Data',
			'label': 'Lead Name',
			'width': 182
		},

		{
			'fieldname': 'lead_owner',
			'fieldtype': 'Data',
			'label': 'Lead Owner',
			'width': 182
		},

		{
			'fieldname': 'territory',
			'fieldtype': 'Link',
			'label': 'Territory',
			'options': 'Territory',
			'width': 182
		},

		{
			'fieldname': 'status',
			'fieldtype': 'Data',
			'label': 'Status',
			'width': 182
		},

		{
			'fieldname': 'contact_number',
			'fieldtype': 'Data',
			'label': 'Contact Number',
			'width': 182
		},

		{
			'fieldname': 'remarks',
			'fieldtype': 'Data',
			'label': 'Remarks',
			'width': 400
		},

		{
			'fieldname':'description',
			'fieldtype':'Small Text',
			'label':'Description',
			'width':400
		},
	]

	return columns

def get_data(filters):

	data = [{}]

	return data