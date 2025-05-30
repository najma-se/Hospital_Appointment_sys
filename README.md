Hospital Appointment Management System

A web-based application designed to streamline the process of booking and managing hospital appointments. Built with Django, the system facilitates patient registrations, appointment requests, approvals by admin staff, and appointment management.

Features

✅ User Authentication
	•	Patients and Admins can register and log in.
	•	Role-based redirection to appropriate dashboards.

✅ Appointment Requests
	•	Patients can request appointments by selecting doctor, date, time, and adding a description.
	•	Admins can approve or reject requests.

✅ Appointment Management
	•	Admins can view and manage confirmed appointments.
	•	Cancel or update appointments if necessary.

✅ Admin Dashboard
	•	View all appointment requests and appointments.
	•	Manage doctors and departments.



Technologies Used:
	•	Backend: Django (Python)
	•	Frontend: HTML, CSS, Bootstrap, JavaScript
	•	Database: SQLite (default)
	•	Version Control: Git & GitHub

 📂 Project Structure

🗂 Project Structure

Hospital_Appointment_sys/
├── appointmentsystem/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/
│   │   ├── admin/
│   │   ├── user/
│   │   └── ...
│   └── static/
├── db.sqlite3
├── manage.py
└── requirements.txt


Installation and Setup

1. Clone the repository:

```git clone https://github.com/najma-se/Hospital_Appointment_sys.git```
```cd Hospital_Appointment_sys```

2. Create a virtual environment:

```python -m venv venv```
```source venv/bin/activate  # On Windows: venv\Scripts\activate```

3. Install dependencies:

```pip install -r requirements.txt```

4. Run database migrations:

```python manage.py makemigrations```
```python manage.py migrate```

5. Create a superuser:

```python manage.py createsuperuser```

6. Run the development server:

```python manage.py runserver```


Usage
	•	Patients can register and log in to book appointments.
	•	Admins can log in, view appointment requests, approve/reject requests, and manage appointments.
	•	Both admins and patients have role-specific dashboards.







