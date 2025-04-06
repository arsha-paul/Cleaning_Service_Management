## Cleanser_calicut

Clean Management System

#### License

mit

# Cleaning Service Management

A professional cleaning management system built using the **Frappe Framework**.

## 📦 Features

- User registration, login, address & location management
- Image upload, square footage input, date selection
- Team and supervisor assignment by Admin
- Work progress tracking & time logging by Team Leads
- Payment status monitoring & feedback handling
- Inventory allocation and report generation

## 🚀 Tech Stack

- Backend: Python, Frappe Framework
- Frontend: Frappe Desk
- Database: MariaDB
- Auth: Frappe's Role-based Permissions
- Deployment: Self-hosted or via Bench

## 🛠 Setup (Developer Guide)

```bash
# Clone the repo
git clone git@github.com:arsha-paul/Cleaning_Service_Management.git

# Navigate into bench and install app
cd version-15-bench
bench get-app cleaning_management ./apps/cleaning_management
bench --site yoursite install-app cleaning_management
