// Copyright (c) 2025, Arsha Paul and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Booking", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Booking", {
    refresh: function (frm) {
        // Remove duplicate buttons to avoid multiple "Proceed to Payment" options
        frm.clear_custom_buttons();

        // // Add "Proceed to Payment" button
        // frm.add_custom_button("Proceed to Payment", function () {
        //     frappe.call({
        //         method: "clean_management.cleanser_calicut.doctype.booking.booking.create_payment_entry",
        //         args: { booking_id: frm.doc.name },
        //         callback: function (response) {
        //             if (response.message) {
        //                 // Redirect directly to the specific Payment entry form
        //                 frappe.set_route("Form", "Payment", response.message);
        //             } else {
        //                 frappe.msgprint("Failed to create Payment record.");
        //             }
        //         }
        //     });
        // }, "Actions");

        

        // Ensure phone number starts with "+91 "
        let phoneField = frm.fields_dict.phone.$wrapper.find("input");
        if (!frm.doc.phone || !frm.doc.phone.startsWith("+91 ")) {
            frm.set_value("phone", "+91 ");
        }

        phoneField.on("focus", function () {
            if (!frm.doc.phone.startsWith("+91 ")) {
                frm.set_value("phone", "+91 ");
            }
            this.setSelectionRange(4, 4);
        });

        phoneField.on("input", function () {
            let phone = this.value;
            if (!phone.startsWith("+91 ")) {
                frm.set_value("phone", "+91 ");
                return;
            }
            let digits = phone.replace(/\D/g, "").substring(2, 12);
            if (digits.length > 10) {
                digits = digits.substring(0, 10);
            }
            frm.set_value("phone", "+91 " + digits);
        });

        phoneField.on("keypress", function (event) {
            if (event.which < 48 || event.which > 57) {
                event.preventDefault();
            }
        });

        phoneField.on("keydown", function (event) {
            if (this.selectionStart < 4 && (event.key === "Backspace" || event.key === "Delete")) {
                event.preventDefault();
            }
        });

        // Date Validation
        frm.fields_dict.date.$wrapper.find("input").on("change", function () {
            let selectedDate = frm.doc.date;
            let today = frappe.datetime.get_today();
            if (selectedDate < today) {
                frappe.msgprint("Date cannot be in the past.");
                frm.set_value("date", today);
            }
        });

        // District & City Selection
        const city_data = {
            "Thiruvananthapuram": ["Thiruvananthapuram", "Neyyattinkara", "Varkala", "Kovalam", "Attingal", "Kilimanoor", "Kazhakoottam", "Poovar"],
            "Kollam": ["Kollam", "Paravur", "Punalur", "Karunagappally", "Kottarakkara", "Anchal", "Chathannoor", "Thenmala"],
            "Pathanamthitta": ["Pathanamthitta", "Thiruvalla", "Adoor", "Ranni", "Konni", "Pandalam"],
            "Alappuzha": ["Alappuzha", "Chengannur", "Cherthala", "Haripad", "Kayamkulam", "Ambalappuzha", "Mavelikkara"],
            "Kottayam": ["Kottayam", "Changanassery", "Pala", "Ettumanoor", "Vaikom", "Kaduthuruthy", "Kanjirappally", "Kumarakom"],
            "Idukki": ["Thodupuzha", "Munnar", "Devikulam", "Peermade", "Kattappana", "Adimali", "Nedumkandam"],
            "Ernakulam": ["Kochi", "Aluva", "Perumbavoor", "Muvattupuzha", "Angamaly", "Kakkanad", "North Paravur"],
            "Thrissur": ["Thrissur", "Irinjalakuda", "Chalakudy", "Kodungallur", "Guruvayur", "Kunnamkulam", "Wadakkanchery"],
            "Palakkad": ["Palakkad", "Ottapalam", "Shoranur", "Chittur", "Mannarkkad", "Alathur"],
            "Malappuram": ["Malappuram", "Manjeri", "Perinthalmanna", "Tirur", "Kottakkal", "Nilambur", "Ponnani"],
            "Kozhikode": ["Kozhikode", "Vadakara", "Kunnamangalam", "Feroke", "Balussery", "Koyilandy", "Chelannur", "Mukkom"],
            "Wayanad": ["Kalpetta", "Sulthan Bathery", "Mananthavady", "Meppadi", "Vythiri"],
            "Kannur": ["Kannur", "Thalassery", "Payyannur", "Mattannur", "Iritty", "Panoor"],
            "Kasaragod": ["Kasaragod", "Kanhangad", "Nileshwar", "Bekal", "Manjeshwar"]
        };

        frm.set_query("city", function () {
            let selectedDistrict = frm.doc.district;
            return {
                filters: {
                    name: ["in", city_data[selectedDistrict] || []]
                }
            };
        });

        frm.fields_dict.district.$wrapper.find("input").on("change", function () {
            let selectedDistrict = frm.doc.district;
            if (selectedDistrict && city_data[selectedDistrict]) {
                frm.set_df_property("city", "options", [" "].concat(city_data[selectedDistrict]));
            } else {
                frm.set_df_property("city", "options", [" "]);
            }
        });
    },

    after_save: function (frm) {
        frappe.call({
            method: "clean_management.cleanser_calicut.doctype.booking.booking.create_payment_entry",
            args: { booking_id: frm.doc.name },
            callback: function (response) {
                if (response.message) {
                    // Redirect directly to the specific Payment form using its ID
                    frappe.set_route("Form", "Payment", response.message);
                } else {
                    frappe.msgprint("Failed to create Payment record.");
                }
            }
        });
    }

    

    
});


// frappe.listview_settings['Booking'] = {
//     add_fields: ["supervisor"],  // Ensure the field is loaded
//     get_indicator: function(doc) {
//         return [__("Assigned"), "green", "supervisor,=," + doc.supervisor];
//     },

//     onload: function (listview) {
//         listview.page.add_inner_button(__('Refresh'), function () {
//             listview.refresh();
//         });
//     },

//     formatters: {
//         supervisor: function (value, df, doc) {
//             if (!value) {
//                 return `<button class="btn btn-primary btn-xs assign-supervisor" data-name="${doc.name}">Assign Supervisor</button>`;
//             }
//             return value;
//         }
//     }
// };

// frappe.listview_settings['Booking'] = {
//     onload: function (listview) {
//         listview.page.add_inner_button(__('Refresh'), function () {
//             listview.refresh();
//         });

//         // Attach event listener after list is rendered
//         listview.on('render', function () {
//             $(".assign-supervisor").remove();  // Avoid duplicates

//             listview.data.forEach(doc => {
//                 let row = $(`[data-name='${doc.name}']`);
                
//                 if (row.length && !row.find('.assign-supervisor').length) {
//                     let button = $(`<button class="btn btn-primary btn-xs assign-supervisor" data-name="${doc.name}">Assign Supervisor</button>`);
                    
//                     button.click(function () {
//                         let booking_name = $(this).data('name');

//                         frappe.db.get_list('Supervisor', { fields: ['name', 'full_name'] }).then(supervisors => {
//                             let options = supervisors.map(sup => ({
//                                 label: sup.full_name,
//                                 value: sup.name
//                             }));

//                             frappe.prompt([
//                                 {
//                                     label: "Select Supervisor",
//                                     fieldname: "supervisor",
//                                     fieldtype: "Select",
//                                     options: options.map(o => o.value).join("\n") // Convert array to string
//                                 }
//                             ], function (values) {
//                                 frappe.db.set_value('Booking', booking_name, 'supervisor', values.supervisor)
//                                     .then(() => {
//                                         frappe.show_alert({ message: "Supervisor Assigned", indicator: "green" });
//                                         listview.refresh();
//                                     });
//                             }, "Assign Supervisor", "Assign");
//                         });
//                     });


//                     // frappe.ui.form.on('Booking', {
//                     //     after_save: function(frm) {
//                     //         // Redirect user to the new payment form with booking ID
//                     //         frappe.set_route("Form", "Payment", );
//                     //     }
//                     // });
                    

//                     // Append button inside the row's last column (Actions)
//                     row.find('.list-row-col:last').append(button);
//                 }
//             });
//         });
//     }
// };
