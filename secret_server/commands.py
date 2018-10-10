# -*- coding: utf-8 -*-
from secret_server.config import Config
import requests
import json

class AccessToken:
    @classmethod
    def get_token(cls):
        with open("creds.json","r") as outfile:
            load = json.load(outfile)

        resp = requests.post(Config.BASE_URL+"/oauth2/token", data=load)
        return resp.json()["access_token"]

class Secret:
    
    @classmethod
    def __get_headers(cls):
        headers = {"Authorization" : "bearer {token}".format(token=AccessToken.get_token()), "Content-Type" : "application/json"}
        return headers

    @classmethod
    def get(cls, id):
        if type(id) == int:
            id = str(id)
        url =  "{base_url}/api/v1/secrets".format(base_url=Config.BASE_URL)
        uri = '{url}/{id}'.format(url=url,id=id)
        resp = requests.get(uri,headers=cls.__get_headers())
        resp.close()
        return resp.json()

    @classmethod
    def get_field(cls, id, field):
        if type(id) == int:
            id = str(id)
        url =  "{base_url}/api/v1/secrets".format(base_url=Config.BASE_URL)
        uri = '{url}/{id}/fields/{field}'.format(url=url, id=id, field=field)
        resp = requests.get(uri, headers=cls.__get_headers())
        resp.close()
        return resp.json()