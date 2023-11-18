frappe.listview_settings['Lead'] = {

	add_fields: ["status"],

	get_indicator: (doc) => {

		if (doc.status == "Open") {
			return [__(doc.status), "purple", "status,=,Open"];
        }

        if (doc.status == "Replied") {
			return [__(doc.status), "blue", "status,=,Replied"];
        }

		else if (doc.status == "Quotation Created") {
			return [__(doc.status), "green", "status,=,Quotation Created"];
		}

		else if (doc.status == "Opportunity Closed") {
			return [__(doc.status), "red", "status,=,Opportunity Closed"];
		}

        else if (doc.status == "Opportunity Open") {
			return [__(doc.status), "green", "status,=,Opportunity Open"];
		}

        else if (doc.status == "Do Not Disturb") {
			return [__(doc.status), "orange", "status,=,Do Not Disturb"];
		}

	},

};