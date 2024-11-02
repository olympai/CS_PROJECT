# In this document you may find important shortcuts and coding helpers as well as common used commands


# Create a virtual environment
python3 -m venv venv

# install all requirements
pip install -r requirements.txt

# Activate a virtual environment
# Windows
venv/scripts/activate
# Mac
venv/bin/activate
If permission denied: chmod +x venv/bin/activate

# Gather all dependencies in the file requirements.txt
pip freeze > requirements.txt

# Git push checklist
git init 
git add .
git commit -m 'Aenderungen'
git remote rename origin old-origin
git remote add origin (link)
git push -u origin main
- Procfile korrekt parsen
- Datenbankzugriff auf postgres umstellen
- Postgres und Redis Credentials überprüfen
- Key-System auf Heroku-Modus umstellen
- Datenbankveränderungen über GO propagieren