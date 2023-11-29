frappe.ui.form.on("Opportunity", {

    refresh:  async function(frm) {

        setTimeout(() => {

            frm.remove_custom_button("Supplier Quotation", "Create");
            frm.remove_custom_button("Request For Quotation", "Create");
            frm.remove_custom_button("Customer", "Create");
			frm.remove_custom_button("Quotation", "Create");
            frm.remove_custom_button("Reopen");
            frm.remove_custom_button("Close");

            $("[data-doctype='Request for Quotation']").hide();
            $("[data-doctype='Supplier Quotation']").hide();

        }, 100);

		var opp_value = await frappe.db.get_list("Customer",{filters:{opportunity_name:cur_frm.doc.name}})
		if (!opp_value.length){

			if (!frm.doc.__islocal){
				frm.add_custom_button(__('<p style="color: #171717; padding-top:8px;padding-left:10px;padding-right:10px;"><b>Create Customer</b></p>'), () => {
					var tax_category = ''
					var readvalue = 0
					frappe.call({
						method: "global_safety_enterprises.global_safety_enterprises.utils.py.opportunity.get_lead_addresses",
						args: {
							'lead_name': frm.doc.party_name
						},
						callback: function(response) {
							if (response.message['state']) {
								if (response.message['state']  == 'Tamil Nadu') {
									tax_category = 'In-State'
								}
								else{
									tax_category = 'Out-State'
								}
							}
							else{
								tax_category = 'In-State'
							}
							var dialog = new frappe.ui.Dialog({
								title: __("Create Customer"),
								fields: [
									{fieldtype: "Data", fieldname: "customer_name", label: __("Customer Name"), default:cur_frm.doc.customer_name, reqd: 1},
									{fieldtype: "Select", fieldname: "customer_type", label: __("Customer Type"), options: "Company\nIndividual\nProprietorship\nPartnership", reqd: 1},
									{fieldtype: "Link", fieldname: "customer_group", label: __("Customer Group"), options: "Customer Group"},
				
									{fieldtype: "Link", fieldname: "tax_category", label: __("Tax Category"), default:tax_category,options: "Tax Category", hidden: 1},
								],
							});
							dialog.set_primary_action(__("Save"), function() {
								let values = dialog.get_values();
							
								frappe.call({
									method: "global_safety_enterprises.global_safety_enterprises.utils.py.opportunity.create_customer",
									args: {
										'lead_name': frm.doc.party_name,
										'customer':values.customer_name,
										'type':values.customer_type,
										'group':values.customer_group,
										'tax':values.tax_category,
										'opportunity_name':frm.doc.name,
									},
									callback:function(r){
										frappe.show_alert({message: 'Customer Created Successfully', indicator: 'green' });
										frm.reload_doc()
									}
								});
							
								dialog.hide();
							});
							dialog.show()
						}
					});
				});
			}
    	}
		else{
			
			frm.add_custom_button(__('<p style="color: #171717; padding-top:8px;padding-left:10px;padding-right:10px;"><b>Create Quotation</b></p>'), () => {

				frappe.model.open_mapped_doc({
					method: "global_safety_enterprises.global_safety_enterprises.utils.py.opportunity.make_quotation",
					frm: cur_frm
				})

			})
		}
	},

	custom_ts_status: function(frm){

		frm.set_value("status", frm.doc.custom_ts_status)
	}
});
