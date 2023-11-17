frappe.listview_settings['Opportunity'] = {

	add_fields: ["status"],

	get_indicator: (doc) => {

		if (doc.status == "Open") {
			return [__(doc.status), "purple", "status,=,Open"];
        }

		else if (doc.status == "Quotation Created") {
			return [__(doc.status), "green", "status,=,Quotation Created"];
		}


		else if (doc.status == "Closed") {
			return [__(doc.status), "red", "status,=,Closed"];
		}

	},

};