frappe.ui.form.on("Quotation", {

    refresh: function(frm){

		setTimeout(() => {
			frm.remove_custom_button('Sales Order',"Create");
			frm.remove_custom_button("Set as Lost");
			frm.remove_custom_button("Opportunity", "Get Items From");
		}, 100)
    },

	custom_margin_: function(frm){

		for (var i = 0; i < (frm.doc.items).length; i++){

			frappe.model.set_value(frm.doc.items[i].doctype, frm.doc.items[i].name, "custom_ts_margin", frm.doc.custom_margin_)

		}
	}
})

frappe.ui.form.on("Quotation Item", {

	custom_ts_margin: function(frm, cdt, cdn){

		var data = locals[cdt][cdn]

		frappe.model.set_value(cdt, cdn, "margin_type", "Percentage")
		frappe.model.set_value(cdt, cdn, "margin_rate_or_amount", data.custom_ts_margin)
	},

	item_code: function(frm, cdt, cdn){

		setTimeout(() => {

			frappe.model.set_value(cdt, cdn, "custom_ts_margin", frm.doc.custom_margin_)

		}, 200);
	}
})