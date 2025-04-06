# Copyright (c) 2025, Arsha Paul and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AssignBooking(Document):
	pass


import frappe

@frappe.whitelist()
def get_supervisor_bookings(supervisor):
    """Fetch all bookings assigned to a specific supervisor"""
    if not supervisor:
        frappe.throw("Supervisor ID is required")

    assigned_bookings = frappe.get_all("Assign Booking", 
        filters={"supervisor": supervisor}, 
        fields=["name", "date"]
    )

    for booking in assigned_bookings:
        # Fetch child table entries
        booking["bookings"] = frappe.get_all("Child Assign Booking",
            filters={"parent": booking["name"]},
            fields=["booking_id", "customer_name", "service", "status"]
        )

    return assigned_bookings


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user

    user_roles = frappe.get_roles(user)

    # Admin can see all bookings
    if 'Administrator' in user_roles:
        return None

    # Supervisor should see only their assigned bookings
    if 'Supervisor' in user_roles:
        return """(`tabassigned_bookings`._assign LIKE '%{user}%')""".format(user=user)

    return None
