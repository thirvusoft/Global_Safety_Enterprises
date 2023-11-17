frappe.ui.form.on("Item", {
    refresh: function(frm){
		setTimeout(()=>{
			frm.remove_custom_button("Stock Balance", "View");
			frm.remove_custom_button("Stock Ledger", "View");
            frm.remove_custom_button("Stock Projected Qty", "View");
			frm.remove_custom_button("Add / Edit Prices", "Actions");
            $("[data-doctype='Sales Order']").hide();
            $("[data-doctype='Delivery Note']").hide();
            $("[data-doctype='Sales Invoice']").hide();
            $($("[data-doctype='BOM']")[0].parentElement).hide();
            $($("[data-doctype='Item Price']")[0].parentElement).hide();
            $($("[data-doctype='Material Request']")[0].parentElement).hide();
            $($("[data-doctype='Production Plan']")[0].parentElement).hide();
            $($("[data-doctype='Serial No']")[0].parentElement).hide();
            $($("[data-doctype='Stock Entry']")[0].parentElement).hide();
		},100)
    }
})