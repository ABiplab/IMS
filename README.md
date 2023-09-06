# IMS (Inventory Management System)

This is an Inventory Management System developed using Django, designed to manage inventory records with different user roles and permissions.
## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)


## Features

- Two user roles: Department Manager and Store Manager.
- Role-based permissions for managing inventory records.
- Add, change, and remove inventory records with approval workflows.
- Fetch and approve pending inventory change requests.
- Pagination for the inventory list.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x: [Install Python](https://www.python.org/downloads/)
- Django: Install using `pip install django`
- Django REST framework: Install using `pip install djangorestframework`

## Installation

1. Clone the repository:
    git clone https://github.com/ABiplab/IMS.git or you can download it as zip.
2. Create a virtual environment (recommended):
    python -m venv venv
    in Linux user `source venv/bin/activate`   or on Windows, use `venv\Scripts\activate`
3. Install project dependencies:
    pip install -r requirements.txt
4. Apply database migrations:
    python manage.py migrate
5. Apply database migrations:
    python manage.py runserver
6. Create a superuser for admin access:
    python manage.py createsuperuser
7. Run the development server:
    python manage.py runserver

## Usage
1.Access the Django admin panel at http://localhost:8000/admin/ and log in with the superuser credentials to manage users, roles, and other data.

## API Endpoints
* Login: `/api/api_login/`
* Add Inventory: `/api/add_inventory/`
* Fetch Inventory: `/api/fetch_inventory/`
* Approve Inventory: `/api/approve_inventory/`
* for better reference you can import `IMS.postman_collection.json` in postman for details view
<img width="494" alt="image" src="https://github.com/ABiplab/IMS/assets/35728992/fcea272b-1d91-4add-97c7-add6265d2e90">
*click on import
