# -*- coding: utf-8 -*-
from secret_server.config import Config
import requests
import json

class AccessToken:

    @classmethod
    def get_token(cls):
        __creds = {"grant_type" : "client_credentials"}

        with open("creds.json","r") as outfile:
            load = json.load(outfile)
            __creds["client_id"] = "sdk-client-"+load["clientId"]
            __creds["client_secret"] = load["clientSecret"]

        resp = requests.post(Config.BASE_URL+"/oauth2/token", data=__creds)
        return resp.json()["access_token"]

class Secret:
    
    @classmethod
    def get_secret(cls, id):
        if type(id) == int:
            id = str(id)
        token = AccessToken.get_token()
        headers = {"Authorization" : "bearer "+token, "Content-Type" : "application/json"}
        uri = Config.BASE_URL+"/api/v1/secrets/"
        resp = requests.get(uri+id,headers=headers,)
        return resp.json()