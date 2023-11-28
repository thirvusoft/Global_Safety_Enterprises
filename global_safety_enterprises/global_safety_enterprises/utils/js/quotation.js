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
	},
	custom_view_follow_up_details: function(frm){
		let data=`<table style="font-size:14px; border:1px solid black;width:100%">

			<tr style="font-weight:bold; border:1px solid black; padding:5px;">
				<td style="border:1px solid black; padding:5px;">
				<center>
				    S.No
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Date
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Mode of Communication
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Followed By
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Description
				</center>
				</td>
			</tr>
		`
		frm.doc.custom_followup.forEach(row => {
			data += `
			<tr style="border:1px solid black; padding:5px;">
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.idx}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.date}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.mode_of_communication}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.followed_by}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.description}
				</center>
				</td>
			</tr>
			`
		})
		data += `</table>`
		var d = new frappe.ui.Dialog({
			title: __("Follow Up Details"),
			size:"extra-large",
			fields : [
				{
					fieldname: 'html_data',
					fieldtype: "HTML"
				}
			]
			
		})
		d.show();
		$(d.get_field('html_data').wrapper).html(data) 
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