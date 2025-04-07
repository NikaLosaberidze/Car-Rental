# Car Rental Django Application Documentation

## Overview
This is a minimalist Django web application for car rental services. It allows users to register and log in using their phone number and password, add cars with photos, view available cars, and rent them with a single click.

---

## Project Structure

```
conf/           # Django project root
├── __init.py__                
├── asgi.py/               
├── settings.py/               
├── urls.py/               
├── wsgi.py/              
└── manage.py

media/                # Uploaded images

cars/            # Main Django app
├── admin.py   # Register models
├── apps.py   # App configuration
├── templates/   # HTML templates
├── authentication.py   # For user authentication
├── models.py         # Database models
├── forms.py          # Car forms
└── urls.py           # App-specific routes
└── views.py          # View logic
```

---

## Features
- **Authentication:** Custom user model with phone number as the username.
- **Car Management:** Users can add cars with 3 or less images.
- **Car Listing:** All available cars are displayed on the homepage.
- **Rental:** Authenticated users can rent cars instantly.
- **Profile Page:** Displays user's own cars and rentals.

---

## Static and Media Files

- Uploaded images are stored in `/media/car_images/`
- Ensure this is served correctly by configuring `MEDIA_URL` and `MEDIA_ROOT` in `settings.py`

---

## Running the Project

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. Visit `http://127.0.0.1:8000/`

---

## Notes
- No payment system is implemented.
- Admin panel is available at `/admin/` for superuser access.

---

## License
This project is for academic/demonstration use.

