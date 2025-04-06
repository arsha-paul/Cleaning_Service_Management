# import frappe
# from frappe import _

# def get_context(context):
#     # Get the logged-in user's email
#     user_email = frappe.session.user

#     # Fetch user details from the User doctype
#     user = frappe.db.get_value("User", user_email, 
#         ["email", "full_name", "mobile_no", "location", "user_image", "gender", "birth_date"], as_dict=True)

#     if user:
#         context.user_data = {
#             "email": user.get("email"),
#             "full_name": user.get("full_name"),
#             # "profile_image": user.get("user_image", "/files/default-user.png"),
#             "phone": user.get("mobile_no"),
#             # "gender": user.get("gender"),
#             # "date_of_birth": user.get("birth_date"),
#             "address": user.get("location"),
#         }
#     else:
#         context.user_data = {}

#     context.user = user  # If you still need the `user` object separately


import frappe

def get_context(context):
    # Get logged-in user's email
    user_email = frappe.session.user
    frappe.logger().info(f"Fetching user data for email: {user_email}")

    # Fetch User details
    user = frappe.get_all(
        "User",
        filters={"email": user_email},
        fields=["full_name", "email", "phone", "location"]
    )

    frappe.logger().info(f"User data fetched: {user}")

    # Add data to context
    if user:
        context.user = user[0]
    else:
        context.user = {}
        frappe.logger().warning("No user found for the given email.")