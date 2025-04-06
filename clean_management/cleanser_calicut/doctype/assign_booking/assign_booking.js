// Copyright (c) 2025, Arsha Paul and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Assign Booking", {
// 	refresh(frm) {

// 	},
// });



frappe.listview_settings['Assign Booking'] = {
    onload: function(listview) {
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Supervisor',  // Assuming Supervisor is linked with Employee/User
                filters: { 'user_id': frappe.session.user },
                fieldname: 'name'
            },
            callback: function(response) {
                if (response.message) {
                    let supervisor_name = response.message.name;
                    listview.filter_area.add('Assign Booking', 'supervisor', '=', supervisor_name);
                    listview.refresh();
                }
            }
        });
    }
};


// def get_permission_query_conditions(user):
//     if not user:
//         user = frappe.session.user

//     user_roles = frappe.get_roles(user)

//     # Admin can see all bookings
//     if 'Admin' in user_roles:
//         return None

//     # Supervisor should see only their assigned bookings
//     if 'Supervisors' in user_roles:
//         return """(`tabBooking`._assign LIKE '%{user}%')""".format(user=user)

//     return None



