frappe.ui.form.on("User", {

    refresh: function(frm){

		if (frappe.session.user != "Administrator"){

			setTimeout(() => {
				frm.remove_custom_button("Set User Permissions", "Permissions");
				frm.remove_custom_button("View Permitted Documents", "Permissions");
				frm.remove_custom_button("Reset Password", "Password");
				frm.remove_custom_button("Create User Email");
			}, 100)
		}
    }
})