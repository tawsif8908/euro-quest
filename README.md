# EuroQuest Recruitment Agency

A full-stack recruitment platform with Django REST API backend and static HTML frontend.

## 🚀 Quick Start

### Backend (Django)
```bash
# Start backend server
./start_backend.bat
# Or manually:
# cd backend
# python manage.py runserver
```
Server runs on: `http://127.0.0.1:8000`

### Frontend (Static HTML)
Open `frontend/index.html` with Live Server extension in VS Code.

## 📁 Project Structure

```
euro-quest/
├── backend/              # Django REST API
│   ├── euroquest/        # Django project settings
│   ├── jobs/            # Job postings app
│   ├── applications/    # Job applications app
│   ├── contacts/        # Contact forms app
│   ├── blogs/           # Blog system app
│   ├── manage.py        # Django management script
│   └── requirements.txt  # Python dependencies
├── frontend/            # Static HTML website
│   ├── index.html       # Main page
│   ├── api.js          # Frontend API integration
│   └── assets/         # CSS, images, etc.
└── start_backend.bat   # Windows script to start backend
```

## 🔧 Tech Stack

### Backend
- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Database**: SQLite (development)
- **Features**: CORS, filtering, pagination

### Frontend
- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first styling
- **Vanilla JS**: API integration
- **Responsive**: Mobile-first design

## 📡 API Endpoints

### Jobs
- `GET /api/jobs/` - List/filter jobs
- `POST /api/jobs/` - Create job
- `GET /api/jobs/{id}/` - Job details

### Applications
- `POST /api/applications/` - Submit application
- `GET /api/applications/{id}/` - Application details

### Contacts
- `POST /api/contacts/` - Send message
- `GET /api/contacts/{id}/` - Contact details

### Blogs
- `GET /api/blogs/` - List blog posts
- `GET /api/blogs/{slug}/` - Blog post details

## 🛠 Development Setup

### Prerequisites
- Python 3.8+
- VS Code with Live Server extension

### Backend Setup
```bash
# Create virtual environment
python -m venv backend_env

# Activate environment
backend_env\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Frontend Development
1. Install VS Code Live Server extension
2. Open `frontend/index.html`
3. Click "Go Live" in status bar
4. Server runs on `http://127.0.0.1:5500`

## 🔗 API Integration

Frontend connects to backend via `api.js`:

```javascript
// Load jobs
API.loadJobs();

// Submit application
API.submitApplication(jobId, {
  applicant_name: 'John Doe',
  email: 'john@example.com',
  experience_level: 'mid'
});
```

## 📊 Features

- ✅ Job posting management
- ✅ Job application system
- ✅ Contact form processing
- ✅ Blog with comments
- ✅ Responsive design
- ✅ RESTful API
- ✅ CORS enabled
- ✅ Input validation
- ✅ SQLite database

## 🚀 Deployment

### Backend (Django)
```bash
# Production settings
DEBUG=False
python manage.py collectstatic
# Use gunicorn or similar
```

### Frontend
- Static files served by any web server
- Update API_BASE URL in `api.js` for production

## 📝 License

ISC
