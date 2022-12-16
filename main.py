import base64
import pprint

from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
from typing import Optional

from configs import Settings

app = FastAPI()
runtime_setting = Settings()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/login")
async def login(request: Request, code: Optional[str] = None):
    data = {}
    print(code)
    if code is not None:
        data = await check_to_github(request, oauth=OauthData(code=code))
    return templates.TemplateResponse("login.html", {"request": request, "data": data})


@app.get("/login/github")
async def login_github(request: Request, code: Optional[str] = None):
    data = {}
    print(code)
    if code is not None:
        data = await check_to_github(request, oauth=OauthData(code=code))
    return templates.TemplateResponse("login.html", {"request": request, "data": data})


@app.get("/login/yahoo")
async def login_yahoo(request: Request, code: Optional[str] = None):
    data = {}
    print(code)
    if code is not None:
        data = await check_to_yahoo(request, oauth=OauthData(code=code))
    return templates.TemplateResponse("login.html", {"request": request, "data": data})


@app.get("/login/line")
async def login_line(request: Request, code: Optional[str] = None):
    # https://developers.line.biz/en/docs/line-login/integrate-line-login/#create-a-channel
    data = {}
    if code is not None:
        data = await check_to_line(request, oauth=OauthData(code=code))
        print(data)
    return templates.TemplateResponse("login.html", {"request": request, "data": data})


class OauthData(BaseModel):
    code: str


class AccessToken(BaseModel):
    token_type: Optional[str] = None
    access_token: Optional[str] = None


@app.post("/oauth/github")
async def check_to_github(request: Request, oauth: OauthData):
    # https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps
    access_token = AccessToken()
    github_user = {}
    access_token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    response = requests.post(access_token_url, headers=headers,
                             json={"client_id": runtime_setting.GITHUB_CLIENT_ID,
                                   "client_secret": runtime_setting.GITHUB_CLIENT_SECRET,
                                   "code": oauth.code,
                                   "redirect_uri": runtime_setting.GITHUB_CALLBACK_URL})
    if response.status_code == status.HTTP_200_OK:
        access_token = AccessToken(**response.json())

    if access_token.token_type and access_token.access_token:
        github_user = await get_github_user(access_token)

    return dict(github_user)


@app.get("/oauth/github/uri")
async def oauth_github_uri():
    authorize_uri = 'https://github.com/login/oauth/authorize'
    client_id = runtime_setting.GITHUB_CLIENT_ID
    redirect_uri = runtime_setting.GITHUB_CALLBACK_URL
    location_href = f"{authorize_uri}?client_id={client_id}&redirect_uri={redirect_uri}"
    return {"location_href": location_href}


@app.post("/oauth/yahoo")
async def check_to_yahoo(request: Request, oauth: OauthData):
    # https://developer.yahoo.com/oauth2/guide/
    access_token = AccessToken()
    yahoo_user = {}
    access_token_url = "https://api.login.yahoo.com/oauth2/get_token"
    # encoded = base64.b64encode((runtime_setting.YAHOO_CLIENT_ID + ':' + runtime_setting.YAHOO_CLIENT_SECRET).encode("utf-8"))
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(access_token_url, headers=headers,
                             data={"client_id": runtime_setting.YAHOO_CLIENT_ID,
                                   "client_secret": runtime_setting.YAHOO_CLIENT_SECRET,
                                   "code": oauth.code,
                                   "redirect_uri": runtime_setting.YAHOO_CALLBACK_URL,
                                   "grant_type": "authorization_code"})
    if response.status_code == status.HTTP_200_OK:
        pprint.pprint(response.json())
        access_token = AccessToken(**response.json())
    if access_token.token_type and access_token.access_token:
        yahoo_user = await get_yahoo_user(access_token)

    return yahoo_user


@app.post("/oauth/line")
async def check_to_line(request: Request, oauth: OauthData):
    # https://developers.line.biz/en/docs/line-login/integrate-line-login/
    access_token = AccessToken()
    line_user = {}
    access_token_url = "https://api.line.me/oauth2/v2.1/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(access_token_url, headers=headers,
                             data={"client_id": runtime_setting.LINE_CLIENT_ID,
                                   "client_secret": runtime_setting.LINE_CLIENT_SECRET,
                                   "code": oauth.code,
                                   "redirect_uri": runtime_setting.LINE_CALLBACK_URL,
                                   "grant_type": "authorization_code"})
    if response.status_code == status.HTTP_200_OK:
        access_token = AccessToken(**response.json())
    if access_token.token_type and access_token.access_token:
        line_user = await get_line_user(access_token)
    return line_user


async def get_github_user(access_token: AccessToken):
    headers = {
        "accept": 'application/json',
        "Authorization": f"{access_token.token_type} {access_token.access_token}"
    }
    response = requests.get("https://api.github.com/user", headers=headers)
    if response.status_code == status.HTTP_200_OK:
        return response.json()


async def get_yahoo_user(access_token: AccessToken):
    headers = {
        'Authorization': f'{access_token.token_type} {access_token.access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.get("https://api.login.yahoo.com/openid/v1/userinfo", headers=headers)
    if response.status_code == status.HTTP_200_OK:
        return response.json()


async def get_line_user(access_token: AccessToken):
    headers = {
        'Authorization': f'{access_token.token_type} {access_token.access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.get("https://api.line.me/oauth2/v2.1/userinfo", headers=headers)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
