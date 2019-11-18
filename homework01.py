# Task 1 Помотреть документацию к API Гитхаба.
# Разобраться и вывести список всех репозиториев для конкретного пользователя.

import requests
import json
from base64 import b64encode

def getReposByUserName(name):
    req = requests.get(f'https://api.github.com/users/{name}/repos')
    resp = None
    if req.status_code == 200:
        resp = json.loads(req.text)
    return resp

def listRepos(repos):
    if repos:
        for i in range(len(repos)):
            print(repos[i]['name'])

def getBase(name, secret):
    return b64encode(f'{name}:{secret}'.encode("ascii")).decode("ascii")

def getBaseSecret():
    name = input('NAME:')
    secret = input('TOKEN:')
    return b64encode(f'{name}:{secret}'.encode("ascii")).decode("ascii")

def getAuthHeader(baseStr):
    return {'Authorization': f'Basic {baseStr}'}

def getGithubProfile(baseStr):
    headers = getAuthHeader(baseStr)
    req = requests.get('https://api.github.com/user', headers=headers)
    return json.loads(req.text)

def testBAPostman(baseStr):
    headers = getAuthHeader(baseStr)
    req = requests.get('https://postman-echo.com/basic-auth', headers=headers)
    return json.loads(req.text)

repos = getReposByUserName('Selen34')
listRepos(repos)

# Task 2 Выполнить запрос методом GET к ресурсам, использующим любой тип авторизации через Postman, Python

base = getBase('postman', 'password')
resp = testBAPostman(base)
print(resp)

#github Personal Access Token
#https://github.com/settings/tokens
#https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

base = getBaseSecret()
profile = getGithubProfile(base)
print(profile)