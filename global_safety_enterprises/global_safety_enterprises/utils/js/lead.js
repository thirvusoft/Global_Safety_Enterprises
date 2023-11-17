frappe.ui.form.on("Lead", {
    refresh: function(frm){
		setTimeout(()=>{
			frm.remove_custom_button("Customer", "Create");
			frm.remove_custom_button("Opportunity", "Create");
			frm.remove_custom_button("Prospect", "Create");
            frm.remove_custom_button("Add to Prospect", "Action");
            $("[data-doctype='Prospect']").hide();
		},100)
    }
})