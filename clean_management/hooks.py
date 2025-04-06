app_name = "clean_management"
app_title = "Cleanser_calicut"
app_publisher = "Arsha Paul"
app_description = "Clean Management System"
app_email = "arshapaulash@gmail.com"
app_license = "mit"

import frappe

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "clean_management",
# 		"logo": "/assets/clean_management/logo.png",
# 		"title": "Cleanser_calicut",
# 		"route": "/clean_management",
# 		"has_permission": "clean_management.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/clean_management/css/clean_management.css"
# app_include_js = "/assets/clean_management/js/clean_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/clean_management/css/clean_management.css"
# web_include_js = "/assets/clean_management/js/clean_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "clean_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "clean_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "home/newhome"



# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "clean_management.utils.jinja_methods",
# 	"filters": "clean_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "clean_management.install.before_install"
# after_install = "clean_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "clean_management.uninstall.before_uninstall"
# after_uninstall = "clean_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "clean_management.utils.before_app_install"
# after_app_install = "clean_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "clean_management.utils.before_app_uninstall"
# after_app_uninstall = "clean_management.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "clean_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
}

permission_query_conditions = {
    "assign_booking": "clean_management.assign-booking.get_permission_query_conditions"
}

permission_query_conditions = {
    "cleaning_task_section": "clean_management.cleaning_task_section.get_permission_query_conditions"
}

#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"clean_management.tasks.all"
# 	],
# 	"daily": [
# 		"clean_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"clean_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"clean_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"clean_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "clean_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "clean_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "clean_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# hooks.py

before_request = ["clean_management.api.set_cors_headers"]
after_request = ["clean_management.api.add_cors_headers"]


# Job Events
# ----------
# before_job = ["clean_management.utils.before_job"]
# after_job = ["clean_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"clean_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# website_route_rules = [
#     {"from_route": "/login", "to_route": "cleanser_calicut/www/login.html"}
# ]

# app_include_js = ["/assets/cleanser_calicut/js/login.js"]

# website_route_rules = [
#     {"from_route": "/login", "to_route": "login"}
# ]


web_routes = [
    {"from_route": "/user-dashboard", "to_route": "user_dashboard"}
]


signup_form_template = "clean_management/templates/register.html"

# def after_login(login_manager):
#     user = frappe.get_doc("User", login_manager.user)
    
#     if "Supervisor" in frappe.get_roles(user.name):
#         frappe.local.response["home_page"] = "/supervisor-dashboard"
#     elif "User" in frappe.get_roles(user.name):
#         frappe.local.response["home_page"] = "/user-dashboard"


api_methods = [
    "clean_management.api.register_user"
]


# override_whitelisted_methods = {
#     "frappe.client.get_list": "frappe.client.get_list",
#     "frappe.client.get": "frappe.client.get",
#     "frappe.client.insert": "frappe.client.insert",
#     "frappe.client.delete": "frappe.client.delete"
# }

from frappe import hooks

import frappe

def set_cors_headers():
    """Set CORS headers for all incoming requests."""
    if frappe.request and frappe.request.method == "OPTIONS":
        frappe.local.response.headers["Access-Control-Allow-Origin"] = "*"
        frappe.local.response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        frappe.local.response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        frappe.local.response["status_code"] = 200  # Return a 200 OK for OPTIONS requests
        return frappe.local.response

def add_cors_headers():
    """Add CORS headers to all responses."""
    frappe.local.response.headers["Access-Control-Allow-Origin"] = "*"
    frappe.local.response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    frappe.local.response.headers["Access-Control-Allow-Headers"] = "Content-Type"

# Add the functions to Frappe hooks
def boot_session(bootinfo):
    set_cors_headers()
    add_cors_headers()

# Hook these functions in `hooks.py`
before_request = ["clean_management.utils.set_cors_headers"]

frappe.enqueue(add_cors_headers)


# permission_query_conditions = {
#     "assign_booking": "clean_management.assign-booking.get_permission_query_conditions"
# }

# In your custom app's hooks.py
def get_list_filters():
    return {
        "Cleaning Task": [
            ["supervisor", "=", frappe.session.user]
        ]
    }


def before_save_payment(doc, method):
    if doc.booking:
        booking_amount = frappe.db.get_value("Booking", doc.booking, "amount")
        if not flt(doc.amount) == flt(booking_amount, 2):
            doc.amount = flt(booking_amount, 2)
            frappe.msgprint("Amount auto-corrected to match Booking amount")

frappe.get_doc("DocType", "Payment").on_update = before_save_payment