setTimeout(async ()=>{
    document.querySelector('button[data-label="Create%20Workspace"]')?.remove()
    frappe.realtime.on("get_user_current_location", async ({})=>{
        let cur_location = await get_location();
        frappe.xcall(
            "global_safety_enterprises.global_safety_enterprises.utils.py.location.update_current_location", 
            {
                lat:cur_location["latitude"], 
                long:cur_location["longitude"]
            }
        )
    })
    let cur_location = await get_location();
        frappe.xcall(
            "global_safety_enterprises.global_safety_enterprises.utils.py.location.update_current_location", 
            {
                lat:cur_location["latitude"], 
                long:cur_location["longitude"]
            }
        )
}, 1000)


async function get_location() {
    check_location_permission()
    async function getLocation() {
        let latitude, longitude;
        try {
            let position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject);
            });

            latitude = position.coords.latitude;
            longitude = position.coords.longitude;
        } catch (error) {
            // Handle errors by displaying them as alerts
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    window.alert("User denied the request for Geolocation.");
                    break;
                case error.POSITION_UNAVAILABLE:
                    window.alert("Location information is unavailable.");
                    break;
                case error.TIMEOUT:
                    window.alert("The request to get user location timed out.");
                    break;
                default:
                    window.alert("An unknown error occurred.");
            }
        }
        return {"latitude":latitude, "longitude":longitude}
    }
    return await getLocation();
}
function check_location_permission() {
    if ("geolocation" in navigator) {
        // Geolocation is available
    } else {
        // Geolocation is not available
        window.alert("Geolocation is not supported in this browser.");
    }
}