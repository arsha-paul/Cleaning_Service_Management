import frappe

def set_cors_headers():
    # Ensure frappe.local.response is initialized
    if not frappe.local.response:
        frappe.local.response = frappe._dict()
    
    if "headers" not in frappe.local.response:
        frappe.local.response.headers = {}

    frappe.local.response.headers["Access-Control-Allow-Origin"] = "*"
    frappe.local.response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    frappe.local.response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
