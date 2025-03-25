# Mini Blog

A Django-based mini blog application with user authentication, CRUD operations for posts and comments, and a responsive Bootstrap interface.

## Features

- User authentication (registration, login, logout)
- CRUD operations for blog posts
- Comment system for posts
- Responsive Bootstrap interface
- Admin panel with custom configurations
- Pagination for posts list
- Search and filter capabilities

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Visit http://127.0.0.1:8000/ in your browser

## Project Structure

- `mini_blog/` - Main project directory
- `blog/` - Blog application
  - `models.py` - Database models
  - `views.py` - View logic
  - `urls.py` - URL routing
  - `forms.py` - Form definitions
  - `templates/` - HTML templates 