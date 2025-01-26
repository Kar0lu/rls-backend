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



## Naming convention
https://github.com/naming-convention/naming-convention-guides/blob/master/git/commit-message-naming.md

## Guide to open development enviroment
https://fancy-rule-a93.notion.site/rodowisko-developerskie-12e078cd02fd8014a207e4ec7bd3cab1?pvs=4

## How to prepare database?
Execute following command in order to supply database with initial data:
```docker compose exec -d rls-django-web python3 manage.py loaddata initial_data.json```
