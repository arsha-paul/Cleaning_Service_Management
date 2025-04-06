# Copyright (c) 2025, Arsha Paul and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CleaningTask(Document):
    def before_insert(self):
        # Ensure supervisor is assigned properly if needed
        if not self.supervisor:
            self.supervisor = frappe.session.user


class CleaningTask(Document):
	pass

import frappe

def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user  # Ensure user is set

    user_roles = frappe.get_roles(user)

    # Allow Admin to see all tasks
    if 'Administrator' in user_roles:
        return None

    # For Supervisors, show only their assigned Cleaning Tasks
    if 'Supervisor' in user_roles:
        return f"""(`tabCleaning Task`.supervisor = '{frappe.db.escape(user)}')"""

    return None


# import frappe

# def get_permission_query_conditions(user):
#     if not user:
#         return ""

#     return f"""(`tabCleaning Task`.supervisor = '{frappe.db.escape(user)}')"""

# def has_permission(doc, user):
#     return doc.supervisor == user
