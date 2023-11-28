{% include "india_compliance/gst_india/client_scripts/party.js" %}

frappe.ui.form.on("Lead", {
    refresh: async function(frm){
        india_compliance.set_state_options(frm);

		setTimeout(()=>{

			frm.remove_custom_button("Customer", "Create");
			frm.remove_custom_button("Opportunity", "Create");
			frm.remove_custom_button("Quotation", "Create");
			frm.remove_custom_button("Prospect", "Create");
            frm.remove_custom_button("Add to Prospect", "Action");

            $("[data-doctype='Prospect']").hide();

		},100)

		var opp_value = await frappe.db.get_list("Opportunity",
			{
				filters:{party_name: cur_frm.doc.name}
			}
		)

		if (!frm.doc.__islocal && opp_value.length == 0){
			
			frm.add_custom_button(__('<p style="color: #171717; padding-top:8px;padding-left:10px;padding-right:10px;"><b>Create Opportunity</b></p>'), () => {

				frappe.model.open_mapped_doc({
					method: "erpnext.crm.doctype.lead.lead.make_opportunity",
					frm: frm
				});
			
			});
		}
    },
	status:function(frm){
		if(cur_frm.doc.status == 'Replied'){
			if( !cur_frm.doc.custom_view_follow_up_details_copy || cur_frm.doc.custom_view_follow_up_details_copy.length < 1){
				frappe.show_alert('Minimum 1 row should be filled in Follow Up Table')
				frappe.db.get_value("Lead", {"name": cur_frm.doc.name}, "status", (r) => {
					cur_frm.set_value('status',r.status)
				});			}
		}
		else if(['Opportunity Closed','Opportunity Open','Quotation Created'].includes(cur_frm.doc.status)){

			frappe.show_alert({message:__(`Not Allowed You To Set ${frm.doc.status} - Status Manually.`), indicator:'red'});
			frappe.db.get_value("Lead", {"name": cur_frm.doc.name}, "status", (r) => {
				cur_frm.set_value('status',r.status)
			});

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
		frm.doc.custom_view_follow_up_details_copy.forEach(row => {
			data += `
			<tr style="border:1px solid black; padding:5px;">
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.idx || ""}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.date || ""}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.mode_of_communication || ""}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.followed_by || ""}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.description || ""}
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
