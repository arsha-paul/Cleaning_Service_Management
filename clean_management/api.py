# import frappe
# from frappe.utils.password import update_password
# from frappe import _
# import html
# from frappe.model.document import Document
# import json

# # @frappe.whitelist(allow_guest=True)
# # def register_user():
# #     try:
# #         # Get JSON request data
# #         data = frappe.request.get_data(as_text=True)
# #         if not data:
# #             return {"status": "error", "message": "Invalid request data"}

# #         data = json.loads(data)

# #         # Extract and sanitize input data
# #         full_name = html.escape(data.get("full_name", "").strip())
# #         email = html.escape(data.get("email", "").strip())
# #         phone = html.escape(data.get("phone", "").strip())
# #         password = data.get("password", "").strip()

# #         if not full_name or not email or not phone or not password:
# #             return {"status": "error", "message": "All fields are required."}

# #         print("Registering user:", full_name, email, phone)

# #         # Check if the email already exists
# #         if frappe.db.exists("User", {"email": email}):
# #             return {"status": "error", "message": "User with this email already exists."}

# #         # Create new user
# #         user_doc = frappe.new_doc("User")
# #         user_doc.first_name = full_name
# #         user_doc.email = email
# #         user_doc.phone = phone
# #         user_doc.send_welcome_email = 0
# #         user_doc.flags.ignore_permissions = True
# #         user_doc.append("roles", {"role": "User"})
# #         user_doc.user_type = "System User"
# #         user_doc.insert()

# #         print("in?", user_doc)

# #         # Set password for the user
# #         update_password(email, password)

# #         # Commit transaction
# #         frappe.db.commit()

# #         return {
# #             "status": "success",
# #             "message": "Account created successfully!",
# #             "redirect_url": "/login"
# #         }

# #     except Exception as e:
# #         frappe.db.rollback()
# #         frappe.log_error(frappe.get_traceback(), "Signup Error")
# #         return {"status": "error", "message": f"An error occurred: {str(e)}"}

# @frappe.whitelist(allow_guest=True)
# def register_user():
#     # Initialize debug information
#     debug_info = {
#         "request_received": frappe.utils.now(),
#         "request_data": None,
#         "validation_checks": {},
#         "processing_steps": [],
#         "errors": []
#     }

#     try:
#         # Log the raw request data
#         raw_data = frappe.request.get_data(as_text=True)
#         debug_info["request_data"] = raw_data
#         frappe.logger().debug(f"Raw request data: {raw_data}")

#         if not raw_data:
#             debug_info["errors"].append("Empty request data received")
#             return build_response("error", "Invalid request data", debug_info)

#         try:
#             data = json.loads(raw_data)
#             debug_info["processing_steps"].append("JSON parsed successfully")
#         except json.JSONDecodeError as e:
#             debug_info["errors"].append(f"JSON decode error: {str(e)}")
#             return build_response("error", "Invalid JSON data", debug_info)

#         # Extract and sanitize input data with debug logging
#         fields = ["full_name", "email", "phone", "password"]
#         extracted_data = {}
        
#         for field in fields:
#             if field in data:
#                 extracted_data[field] = html.escape(data.get(field, "").strip())
#                 debug_info["validation_checks"][f"{field}_exists"] = bool(extracted_data[field])
#             else:
#                 extracted_data[field] = ""
#                 debug_info["errors"].append(f"Missing field: {field}")

#         debug_info["processing_steps"].append("Data extracted and sanitized")

#         # Validate required fields
#         missing_fields = [field for field in fields if not extracted_data[field]]
#         if missing_fields:
#             debug_info["errors"].append(f"Missing required fields: {', '.join(missing_fields)}")
#             return build_response("error", "All fields are required.", debug_info)

#         debug_info["processing_steps"].append("Required fields validated")

#         # Email validation
#         if not frappe.utils.validate_email_address(extracted_data["email"]):
#             debug_info["errors"].append("Invalid email format")
#             return build_response("error", "Please enter a valid email address.", debug_info)

#         # Phone validation
#         phone_pattern = r'^[0-9]{10,12}$'
#         if not frappe.utils.validate_phone_number(extracted_data["phone"], phone_pattern):
#             debug_info["errors"].append("Invalid phone format")
#             return build_response("error", "Please enter a valid phone number (10-12 digits).", debug_info)

#         debug_info["processing_steps"].append("Email and phone validated")

#         # Check if user already exists
#         if frappe.db.exists("User", {"email": extracted_data["email"]}):
#             debug_info["errors"].append("User with this email already exists")
#             return build_response("error", "User with this email already exists.", debug_info)

#         debug_info["processing_steps"].append("User existence checked")

#         # Create new user
#         try:
#             user_doc = frappe.new_doc("User")
#             user_doc.first_name = extracted_data["full_name"]
#             user_doc.email = extracted_data["email"]
#             user_doc.phone = extracted_data["phone"]
#             user_doc.send_welcome_email = 0
#             user_doc.flags.ignore_permissions = True
#             user_doc.append("roles", {"role": "User"})
#             user_doc.user_type = "System User"
            
#             debug_info["processing_steps"].append("User document prepared")
#             frappe.logger().debug(f"User doc before insert: {user_doc.as_dict()}")

#             user_doc.insert()
#             debug_info["processing_steps"].append("User document inserted")

#             # Set password
#             update_password(user_doc.name, extracted_data["password"])
#             debug_info["processing_steps"].append("Password updated")

#             # Commit transaction
#             frappe.db.commit()
#             debug_info["processing_steps"].append("Transaction committed")

#             frappe.logger().debug(f"User created successfully: {user_doc.name}")
#             return build_response("success", "Account created successfully!", debug_info, {"redirect_url": "/login"})

#         except Exception as e:
#             frappe.db.rollback()
#             debug_info["errors"].append(f"User creation error: {str(e)}")
#             frappe.logger().error(f"User creation failed: {frappe.get_traceback()}")
#             return build_response("error", f"An error occurred during registration: {str(e)}", debug_info)

#     except Exception as e:
#         frappe.db.rollback()
#         debug_info["errors"].append(f"Unexpected error: {str(e)}")
#         frappe.logger().error(f"Unexpected error in registration: {frappe.get_traceback()}")
#         return build_response("error", "An unexpected error occurred. Please try again.", debug_info)

# def build_response(status, message, debug_info=None, extra_data=None):
#     response = {
#         "status": status,
#         "message": _(message),
#         "timestamp": frappe.utils.now()
#     }
    
#     if extra_data:
#         response.update(extra_data)
    
#     # Only include debug info in development mode
#     if frappe.conf.get("developer_mode") and debug_info:
#         response["debug_info"] = debug_info
    
#     frappe.logger().debug(f"Returning response: {response}")
#     return response


# @frappe.whitelist()
# def get_username():
#     """
#     Fetches the logged-in user's username.
#     """
#     try:
#         user_email = frappe.session.user  # Get logged-in user's email

#         if not user_email or user_email == "Guest":
#             return {"username": "User"}  # Default if user is not logged in

#         user = frappe.get_doc("User", user_email)  # Fetch User doctype
#         username = user.first_name if user.first_name else "User"

#         return {"username": username}  # Return the first name

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Get Username Error")
#         return {"username": "User"}  # Default on error

# @frappe.whitelist()
# def logout_user():
#     """
#     Logs out the current user and redirects to the home page.
#     """
#     try:
#         frappe.local.login_manager.logout()  # Perform logout
#         frappe.db.commit()  # Ensure changes are saved

#         return {
#             "status": "success",
#             "message": "Logged out successfully!",
#             "redirect_url": "/"  # Redirect to home page
#         }

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Logout Error")
#         return {
#             "status": "error",
#             "message": "An error occurred while logging out."
#         }

# # ------------------------ Helper Functions ------------------------
# def create_success_response(message, file_url=None, redirect_url=None):
#     """
#     Helper function for success responses.
#     """
#     response = {"status": "success", "message": message}
#     if file_url:
#         response["file_url"] = file_url
#     if redirect_url:
#         response["redirect_url"] = redirect_url

#     set_cors_headers()
#     return response, 200

# def create_error_response(error_message):
#     """
#     Helper function for error responses.
#     """
#     set_cors_headers()
#     return {"status": "error", "message": error_message}, 400

# def set_cors_headers():
#     """
#     Sets CORS headers for API responses.
#     """
#     frappe.local.response.headers.update({
#         "Access-Control-Allow-Origin": "*",
#         "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
#         "Access-Control-Allow-Headers": "Content-Type"
#     })


# @frappe.whitelist(allow_guest=False)
# def update_user_profile(full_name, phone, location):
#     try:
#         frappe.logger().info(f"Updating profile for: {frappe.session.user}")

#         user_email = frappe.session.user
#         user_doc = frappe.get_doc("User", user_email)

#         frappe.logger().info(f"Current Data: {user_doc.full_name}, {user_doc.phone}, {user_doc.location}")

#         user_doc.full_name = full_name
#         user_doc.phone = phone
#         user_doc.location = location

#         user_doc.save()
#         frappe.db.commit()

#         return {"success": True, "message": _("Profile updated successfully")}

#     except frappe.DoesNotExistError:
#         frappe.logger().error("User not found!")
#         return {"success": False, "message": _("User not found")}

#     except Exception as e:
#         frappe.logger().error(f"Error updating profile: {str(e)}")
#         return {"success": False, "message": _("Error updating profile")}



# # ------------------------ Booking Document Class ------------------------
# class Booking(Document):
#     pass

# # ------------------------ Create Booking API ------------------------
# @frappe.whitelist(allow_guest=True)
# def create_booking():
#     try:
#         # Debugging logs
#         frappe.logger().info("API called: create_booking")

#         # Extract form data safely
#         booking_data = frappe.request.form.to_dict()
#         frappe.logger().info(f"Extracted Form Data: {booking_data}")

#         # Check for required fields
#         required_fields = ["service_type", "username", "phone", "date", "location", "sqft", "address", "district", "city"]
#         missing_fields = [field for field in required_fields if not booking_data.get(field)]

#         if missing_fields:
#             return create_error_response(f"Missing fields: {', '.join(missing_fields)}")

#         # Check if file is uploaded
#         if "image" not in frappe.request.files:
#             return create_error_response("Image file is missing!")

#         # Read uploaded file
#         uploaded_file = frappe.request.files["image"]
#         file_content = uploaded_file.read()

#         # Debug: Log file details
#         frappe.logger().info(f"Uploaded File: {uploaded_file.filename}, Size: {len(file_content)} bytes")

#         # Save the file in Frappe
#         file_doc = save_file(
#             uploaded_file.filename,
#             file_content,
#             "Booking",
#             None,
#             is_private=0
#         )

#         # Create a new Booking document
#         booking_doc = frappe.get_doc({
#             "doctype": "Booking",
#             "service_type": booking_data.get("service_type"),
#             "username": booking_data.get("username"),
#             "phone": booking_data.get("phone"),
#             "date": booking_data.get("date"),
#             "location": booking_data.get("location"),
#             "image": file_doc.file_url,  # Save file URL
#             "sqft": int(booking_data.get("sqft", 0)),  # Default sqft to 0 if missing
#             "address": booking_data.get("address"),
#             "special_instructions": booking_data.get("special_instructions", ""),  # Default to empty
#             "district": booking_data.get("district"),
#             "city": booking_data.get("city"),
#         })

#         # Insert the document into the database
#         booking_doc.insert(ignore_permissions=True)
#         frappe.db.commit()

#         return create_success_response("Booking created successfully!", file_url=file_doc.file_url)

#     except Exception as e:
#         frappe.logger().error(f"Booking API Error: {frappe.get_traceback()}")
#         return create_error_response(str(e))

# # ------------------------ Helper Functions ------------------------
# def create_success_response(message, file_url=None, redirect_url=None):
#     """
#     Helper function for success responses.
#     """
#     response = {"status": "success", "message": message}
#     if file_url:
#         response["file_url"] = file_url
#     if redirect_url:
#         response["redirect_url"] = redirect_url

#     set_cors_headers()
#     return response, 200

# def create_error_response(error_message):
#     """
#     Helper function for error responses.
#     """
#     set_cors_headers()
#     return {"status": "error", "message": error_message}, 400

# def set_cors_headers():
#     """
#     Sets CORS headers for API responses.
#     """
#     frappe.local.response.headers.update({
#         "Access-Control-Allow-Origin": "*",
#         "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
#         "Access-Control-Allow-Headers": "Content-Type"
#     })


# @frappe.whitelist(allow_guest=True)
# def create_payment():
#     try:
#         data = frappe.form_dict
#         new_payment = frappe.get_doc({
#             "doctype": "Payment",
#             "user": data.get("user"),
#             "booking": data.get("booking"),
#             "amount": data.get("amount"),
#             "payment_status": data.get("payment_status"),
#             "payment_method": data.get("payment_method"),
#             "payment_date": data.get("payment_date")
#         })
#         new_payment.insert(ignore_permissions=True)
#         frappe.db.commit()
#         return {"message": "Payment successful", "payment_id": new_payment.name}
#     except Exception as e:
#         frappe.log_error(f"Payment Error: {str(e)}")
#         return {"error": str(e)}


# # feedback


# import frappe
# from frappe.model.document import Document

# @frappe.whitelist(allow_guest=True)
# def create_feedback(user, rating, review):
#     feedback = frappe.get_doc({
#         "doctype": "Feedback",
#         "user": user,
#         "rating": rating,
#         "review": review,
#         "feedback_date": frappe.utils.today()
#     })
#     feedback.insert(ignore_permissions=True)
#     frappe.db.commit()
#     return {"message": "Feedback submitted successfully"}


import frappe

@frappe.whitelist(allow_guest=True)
def get_feedbacks():
    """Fetch all feedbacks to display on the front page"""
    try:
        feedbacks = frappe.get_all("Feedbacks",  # Ensure "Feedbacks" is the correct doctype
            fields=["name", "username", "rate", "feedback", "date"],
            order_by="date desc",
            limit=10
        )
        return {"status": "success", "feedbacks": feedbacks}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Feedback Retrieval Failed")
        return {"status": "error", "message": str(e)}
