# Copyright (c) 2025, Arsha Paul and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.utils import today


class Booking(Document):
	pass


import frappe
from frappe.model.document import Document
import re

class Booking(Document):
    def validate(self):
        """Validation for Booking form: phone format, required fields, sqft, date, district-city validation."""

        # ----------------- Phone Number Validation -----------------
        if self.get("phone"):
            phone = self.phone.strip()  # Remove extra spaces

            if not phone.startswith("+91 "):
                frappe.throw("Phone number must start with '+91 ' (with a space after +91).")

            # Extract only digits after "+91 "
            phone_digits = re.sub(r"\D", "", phone)[2:]  # Remove non-numeric characters

            if len(phone_digits) != 10:
                frappe.throw("Phone number must contain exactly 10 digits after '+91 '.")

        # ----------------- Required Fields Validation -----------------
        required_fields = ["username", "phone", "service_type", "date", "address", "district", "city"]
        for field in required_fields:
            if not self.get(field):
                frappe.throw(f"{field.replace('_', ' ').title()} is required.")

        # ----------------- Date Validation -----------------
        if self.get("date"):
            today = frappe.utils.today()
            if self.date < today:
                frappe.throw("Date cannot be in the past.")

        # ----------------- Sqft Validation -----------------
        if self.get("sqft") is not None:
            try:
                sqft_value = float(self.sqft)
                if sqft_value <= 0:
                    frappe.throw("Square footage (Sqft) must be a positive number.")
            except ValueError:
                frappe.throw("Sqft must be a valid number.")

        # ----------------- District & City Validation -----------------
        city_data = {
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
        }

        selected_district = self.get("district")
        selected_city = self.get("city")

        if selected_district and selected_city:
            if selected_district not in city_data:
                frappe.throw(f"Invalid district: {selected_district}. Please select a valid district.")

            if selected_city not in city_data[selected_district]:
                frappe.throw(f"Invalid city '{selected_city}' for district '{selected_district}'. Please select a valid city.")

    def after_insert(self):
        """Ensure payment status is set to None when booking is created"""
        frappe.db.set_value("Booking", self.name, "payment_status", None)
        frappe.db.commit()

# @frappe.whitelist()
# def create_payment_entry(booking_id=None):
#     """Creates a payment entry for a given Booking ID"""
#     if not booking_id:
#         return {"status": "error", "message": "Booking ID is required."}

#     try:
#         booking = frappe.get_doc("Booking", booking_id)

#         payment_entry = frappe.get_doc({
#             "doctype": "Payment",
#             "user": booking.username,
#             "payment_date": booking.date,
#             "booking": booking.name,
#             "status": "Pending"
#         })
#         payment_entry.insert(ignore_permissions=True)
#         frappe.db.commit()  # Ensure data is saved

#         return {"status": "success", "payment_id": payment.name}  # Return Payment name for redirection

#     except Exception as e:
#         frappe.log_error(f"Payment Entry Error: {str(e)}", "create_payment_entry")
#         return {"status": "error", "message": str(e)}


# import frappe
# from frappe.utils.file_manager import save_file


@frappe.whitelist()
def create_payment_entry(booking_id=None):
    '''Create a Payment document mapped from Booking.'''

    if not frappe.db.exists('Booking', booking_id):
        frappe.throw(_("Invalid Booking ID: {0}").format(booking_id))

    booking = frappe.get_doc('Booking', booking_id)  # lowercase variable
    
    

    doc = frappe.get_doc({
        'doctype': 'Payment',
        'booking': booking_id,
        'payment_date': today()  # Use the correct variable name
    })
    doc.booking_id = booking.name  # Assign booking_id after creating the document

    doc.insert(ignore_permissions=True)  # Uncomment this line to insert the document
    return doc.name




@frappe.whitelist()
def create_booking():
    try:
        # Debug: Log request data
        frappe.logger().info(f"Request Form Data: {frappe.request.form}")
        frappe.logger().info(f"Request Files: {frappe.request.files}")

        # Check if files are present in the request
        if not frappe.request.files:
            return {"error": "No files found in the request!"}

        # Get the uploaded file
        uploaded_file = frappe.request.files.get("image")
        if not uploaded_file:
            return {"error": "Image file is missing!"}

        # Debug: Log file details
        frappe.logger().info(f"Uploaded File: {uploaded_file.filename}, Size: {len(uploaded_file.read())} bytes")

        # Save the file in Frappe
        file_doc = save_file(
            uploaded_file.filename,
            uploaded_file.read(),
            "Booking",
            None,
            is_private=0
        )

        # Extract form data
        booking_data = frappe.request.form

        # Debug: Log extracted form data
        frappe.logger().info(f"Extracted Form Data: {booking_data}")

        # Create a new Booking document
        booking_doc = frappe.get_doc({
            "doctype": "Booking",
            "service_type": booking_data.get("service_type"),
            "username": booking_data.get("username"),
            "phone": booking_data.get("phone"),
            "date": booking_data.get("date"),
            "location": booking_data.get("location"),
            "image": file_doc.file_url,  # Save the file URL
            "sqft": int(booking_data.get("sqft")),  # Ensure sqft is an integer
            "address": booking_data.get("address"),
            "special_instructions": booking_data.get("special_instructions"),
            "district": booking_data.get("district"),
            "city": booking_data.get("city")
        })

        # Insert the document into the database
        booking_doc.insert(ignore_permissions=True)

        # Commit the transaction
        frappe.db.commit()

        # Return the redirect URL in the response
        return {
            "message": "Booking created successfully!",
            "redirect_url": f"/app/payment/new-payment?booking={booking_doc.name}"
        }

    except Exception as e:
        frappe.logger().error(f"Booking API Error: {frappe.get_traceback()}")
        return {"error": str(e)}