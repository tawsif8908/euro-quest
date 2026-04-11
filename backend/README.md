# EuroQuest Django Backend

A comprehensive Django REST API backend for the EuroQuest Recruitment Agency.

## Features

- **Job Management**: Create, read, update, and delete job postings with filtering
- **Application System**: Handle job applications with status tracking
- **Contact Forms**: Process contact form submissions with response tracking
- **Blog System**: Manage blog posts with comments and categories
- **RESTful API**: Clean Django REST Framework endpoints
- **CORS Support**: Configured for frontend integration
- **Filtering & Pagination**: Advanced filtering and pagination support

## Tech Stack

- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Filtering**: django-filter
- **CORS**: django-cors-headers
- **Environment**: python-decouple

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

## Installation

1. **Create Virtual Environment**
   ```bash
   python -m venv backend_env
   backend_env\Scripts\activate  # Windows
   # source backend_env/bin/activate  # Linux/Mac
   ```

2. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   - Copy `.env` file and update values:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

The server will run on `http://localhost:8000`

## API Endpoints

### Jobs
- `GET /api/jobs/` - List jobs (with filtering)
- `POST /api/jobs/` - Create job
- `GET /api/jobs/{id}/` - Get job details
- `PUT /api/jobs/{id}/` - Update job
- `DELETE /api/jobs/{id}/` - Delete job
- `GET /api/jobs/meta/` - Get job metadata

### Applications
- `GET /api/applications/` - List applications
- `POST /api/applications/` - Submit application
- `GET /api/applications/{id}/` - Get application
- `PUT /api/applications/{id}/` - Update application
- `PATCH /api/applications/{id}/update_status/` - Update status
- `GET /api/applications/by_job/?job_id={id}` - Get applications for job

### Contacts
- `GET /api/contacts/` - List contacts
- `POST /api/contacts/` - Send contact message
- `GET /api/contacts/{id}/` - Get contact
- `PUT /api/contacts/{id}/` - Update contact
- `POST /api/contacts/{id}/respond/` - Add response
- `PATCH /api/contacts/{id}/update_status/` - Update status

### Blogs
- `GET /api/blogs/` - List published blog posts
- `POST /api/blogs/` - Create blog post
- `GET /api/blogs/{slug}/` - Get blog post by slug
- `PUT /api/blogs/{id}/` - Update blog post
- `POST /api/blogs/{id}/like/` - Like blog post
- `POST /api/blogs/{id}/add_comment/` - Add comment
- `GET /api/blogs/meta/` - Get blog metadata

## Frontend Integration

The API is configured with CORS for your frontend. Update `ALLOWED_HOSTS` in settings if needed.

### Example API Calls

```javascript
// Fetch jobs
fetch('http://localhost:8000/api/jobs/')
  .then(res => res.json())
  .then(data => console.log(data));

// Submit job application
fetch('http://localhost:8000/api/applications/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    job: 1,
    applicant_name: 'John Doe',
    email: 'john@example.com',
    experience_level: 'mid'
  })
});
```

## Database Models

### Job
- title, company, location, job_type, category
- description, requirements, salary fields
- contact_email, application_deadline, is_active, featured

### Application
- job (ForeignKey), applicant details
- resume, cover_letter, experience_level
- skills, availability, status

### Contact
- name, email, subject, message, contact_type
- status, priority, response tracking

### Blog
- title, slug, excerpt, content, author info
- category, tags, featured_image
- status, published_at, views, likes, comments

## Development

### Project Structure
```
backend/
├── euroquest/          # Main Django project
├── jobs/              # Jobs app
├── applications/      # Applications app
├── contacts/          # Contacts app
├── blogs/             # Blogs app
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
├── .env              # Environment variables
└── README.md         # This file
```

### Adding New Features

1. Create new Django app: `python manage.py startapp new_app`
2. Add to `INSTALLED_APPS` in settings
3. Create models, serializers, views
4. Add URLs to main `urls.py`

### API Testing

Use Django REST Framework's browsable API at `http://localhost:8000/api/`

### Admin Interface

Access Django admin at `http://localhost:8000/admin/` (requires superuser)

## Deployment

1. Set `DEBUG=False` in production
2. Use PostgreSQL/MySQL database
3. Configure static files serving
4. Set up proper SECRET_KEY
5. Use gunicorn/uwsgi for production server

## Contributing

1. Follow Django best practices
2. Add proper validation to serializers
3. Update this README for new features
4. Test API endpoints thoroughly

## License

ISC