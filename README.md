# Remote Lab System Backend
## Authors
- Kacper Capiga
- Karol Godlewski
- Karol Pacwa

## Creating a Virtual Environment
### Windows
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
### Linux/ macOS
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Naming convention
https://github.com/naming-convention/naming-convention-guides/blob/master/git/commit-message-naming.md

## Guide to open development enviroment
https://fancy-rule-a93.notion.site/rodowisko-developerskie-12e078cd02fd8014a207e4ec7bd3cab1?pvs=4

## How to prepare database?
From rls directory execute following:
```
python manage.py makemigrations
python manage.py migrate
```

## How to wiev docs?
In order to view auto-generated documentation do the following:
```
pip install -r requirements.txt
python manage.py createsuperuser
python manage.py runserver
```
After issuing second command you will be prompted to provide: username (required; default 'root'), email (optional), password (required)
Open application followed by "/admin/doc" and log in using superuser account you created before
