frappe.ui.form.on("Quotation", {

    refresh: function(frm){

		setTimeout(() => {
			frm.remove_custom_button('Sales Order',"Create");
			frm.remove_custom_button("Set as Lost");
			frm.remove_custom_button("Opportunity", "Get Items From");
		}, 100)
    }
})