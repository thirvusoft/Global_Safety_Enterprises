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
		if(frm.doc.last_latitude && frm.doc.last_longitude){
            var map = frm.get_field("map").map;
            var latlng = L.latLng({'lat':frm.doc.last_latitude, 'lng': frm.doc.last_longitude});
            var marker = L.marker(latlng);
                        
            map.flyTo(latlng, 17);
            marker.addTo(map);
        }
    }
})