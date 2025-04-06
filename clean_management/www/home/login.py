import frappe
from frappe.utils import get_url

def get_context(context):
    redirect_to = frappe.local.request.args.get("redirect-to", "/login#signup")
    context.redirect_to = get_url(redirect_to)
