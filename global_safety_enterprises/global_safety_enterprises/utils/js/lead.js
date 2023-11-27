frappe.ui.form.on("Lead", {

    refresh: function(frm){

		setTimeout(()=>{

			frm.remove_custom_button("Customer", "Create");
			frm.remove_custom_button("Opportunity", "Create");
			frm.remove_custom_button("Quotation", "Create");
			frm.remove_custom_button("Prospect", "Create");
            frm.remove_custom_button("Add to Prospect", "Action");

            $("[data-doctype='Prospect']").hide();

		},100)

		frm.add_custom_button(__('<p style="color: #171717; padding-top:8px;padding-left:10px;padding-right:10px;"><b>Create Opportunity</b></p>'), () => {

			frappe.model.open_mapped_doc({
				method: "erpnext.crm.doctype.lead.lead.make_opportunity",
				frm: frm
			});
		 
		});
    }
})