frappe.ui.form.on("Address", {
    setup:function(frm){
		frappe.realtime.on('after_save_address', frm => {
            frappe.run_serially([
                () => frappe.timeout(1),
                () => {
                    console.log('===    ')
                    const last_doc = frappe.contacts.get_last_doc(cur_frm);
                    if (
                        frappe.dynamic_link &&
                        frappe.dynamic_link.doc &&
                        frappe.dynamic_link.doc.name == last_doc.docname
                    ) {
                        for (let i in cur_frm.doc.links) {
                            let link = cur_frm.doc.links[i];
                            if (
                                last_doc.doctype == link.link_doctype &&
                                last_doc.docname == link.link_name
                            ) {
                                frappe.set_route("Form", last_doc.doctype, last_doc.docname);
                            }
                        }
                    }
                },
            ]);
			
		})
	},
})
