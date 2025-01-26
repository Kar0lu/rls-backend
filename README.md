# Remote Lab System Backend
## Authors
- Kacper Capiga
- Karol Godlewski
- Karol Pacwa

## Starting application
### Prerequisites
- Installed Docker (installation instructions available here: https://www.docker.com/get-started/)
### Linux/MacOS
- Clone this repository using ```git clone https://github.com/Kar0lu/rls-backend.git```.
- Open favourite terminal and from root of repository execute following lines:
```
source .env
docker compose up
```
If you pulled from origin and want to build fresh Docker image instead of using ```docker compose up``` invoke ```docker compose up --build``` (full list of available options: https://docs.docker.com/reference/cli/docker/compose/up/).
### Windows
- Clone this repository using ```git clone https://github.com/Kar0lu/rls-backend.git```.
- Open CMD (do not use PowerShell) and from root of repository execute following lines:
```
call .env.bat
docker compose up
```
If you pulled from origin and want to build fresh Docker image instead of using ```docker compose up``` invoke ```docker compose up --build``` (full list of available options: https://docs.docker.com/reference/cli/docker/compose/up/).


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
