// Copyright (c) 2025, Arsha Paul and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Payment", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Payment', {
    onload: function(frm) {
        let params = frappe.utils.get_url_params();
        if (params.booking) {
            frm.set_value("booking", params.booking);
            frm.refresh_field("booking");
        }
    }
});
