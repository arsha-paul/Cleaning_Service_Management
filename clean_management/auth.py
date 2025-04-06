import frappe
import json

@frappe.whitelist(allow_guest=True)
def sign_up(full_name, email, phone, password, role_profile):
    """
    Handles user registration and assigns roles.
    """
    if frappe.db.exists("User", email):
        return {"status": "error", "message": "Email already registered"}
    
    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": full_name,
        "phone": phone,
        "enabled": 1,
        "new_password": password,
        "role_profile_name": role_profile  # Assigning role
    })
    user.insert(ignore_permissions=True)
    
    return {"status": "success", "message": "Account created successfully"}

def get_context(context):
    """
    Context processor for dashboard redirection.
    """
    context.no_cache = 1
    user = frappe.session.user

    if user == 'Guest':
        return
    elif user == 'Administrator':
        frappe.local.flags.redirect_location = "/app"
        raise frappe.Redirect
    else:
        # Check the user's role
        user_role = frappe.db.get_value("User", user, "role_profile_name")
        if user_role == "Supervisor":
            frappe.local.flags.redirect_location = "/supervisor_dashboard"
        elif user_role == "User":
            frappe.local.flags.redirect_location = "/user_dashboard"
        else:
            frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect

def get_routes():
    """
    Define the routes for the application.
    """
    return [
        {
            "path": "/supervisor_dashboard",
            "template": "supervisor_dashboard",  # Path to supervisor dashboard in www folder
            "context": get_context
        },
        {
            "path": "/user_dashboard",
            "template": "user_dashboard",  # Path to user dashboard in www folder
            "context": get_context
        }
    ]
