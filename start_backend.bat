@echo off
echo Starting EuroQuest Django Backend...
cd "c:\Web Projects\euro-quest"
call backend_env\Scripts\activate
cd backend
python manage.py runserver
pause