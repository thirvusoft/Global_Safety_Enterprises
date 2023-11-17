frappe.ui.form.on("Customer", {
    refresh: function(frm){
		setTimeout(()=>{
			frm.remove_custom_button("Accounts Receivable", "View");
			frm.remove_custom_button("Accounting Ledger", "View");
			frm.remove_custom_button("Get Customer Group Details", "Actions");
            frm.remove_custom_button("Pricing Rule", "Create");
            $($("[data-doctype='Sales Order']")[0].parentElement).hide();
            $($("[data-doctype='Payment Entry']")[0].parentElement).hide();
            $($("[data-doctype='Issue']")[0].parentElement).hide();
            $($("[data-doctype='Project']")[0].parentElement).hide();
            $($("[data-doctype='Pricing Rule']")[0].parentElement).hide();
            $($("[data-doctype='Subscription']")[0].parentElement).hide();
            $($("[data-doctype='Party Specific Item']")[0].parentElement).hide();
		},100)
    }
})