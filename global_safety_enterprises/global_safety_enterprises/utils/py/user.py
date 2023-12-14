import frappe

def user_permission_create(doc, action=None):
    if doc.role_profile_name:
        user_permission_list = frappe.get_all("User Permission", filters={"user":doc.name, "allow": "User", 
                            "for_value":doc.name, "apply_to_all_doctypes":1}, fields=["name", "user", "for_value"])
        if not user_permission_list:
            user_permission_check = frappe.db.get_value("Role Profile", doc.role_profile_name, "custom_user_permission")
            if user_permission_check :
                user_permission=frappe.new_doc("User Permission")
                user_permission.update(
                    {
                        "user":doc.name,
                        "allow":"User",
                        "for_value":doc.name,
                        "apply_to_all_doctypes":1,
                    })
                try:
                    user_permission.save()
                    frappe.db.commit()
                    doc.reload()

                except frappe.ValidationError as e:
                    message=e
                    frappe.log_error(title=doc.name, message=e)
        else:
            user_permission_check = frappe.db.get_value("Role Profile", doc.role_profile_name, "custom_user_permission")
            if not user_permission_check:
                frappe.delete_doc("User Permission", user_permission_list[0].name)
        
            if  doc.missed_followup or doc.followup_report:
                user_permission_list = frappe.get_all("User Permission", filters={"user":doc.name, "allow": "User", 
                                "for_value":doc.name, "apply_to_all_doctypes":1}, fields=["name", "user", "for_value"])
                for i in user_permission_list:
                        frappe.delete_doc("User Permission", i.name)
