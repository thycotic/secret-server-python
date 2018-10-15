# -*- coding: utf-8 -*-
# from secret_server.config import Config
import requests
import json
import os

from secret_server.data_protection import DataProtection

if os.path.exists("client_info.json"):
    with open("client_info.json", "r") as outfile:
        BASE_URL = json.load(outfile)["endpoint"]
        URL = "{base_url}/api/v1/secrets".format(base_url=BASE_URL)

class AccessToken:

    @classmethod
    def get_token(cls):
        creds = DataProtection().decrypt()
        resp = requests.post(BASE_URL+"/oauth2/token", data=creds)
        resp.close()
        creds = None
        return resp.json()["access_token"]

class Secret:

    @classmethod
    def __get_headers(cls):
        headers = {"Authorization" : "bearer {token}".format(token=AccessToken.get_token()), "Content-Type" : "application/json"}
        return headers

    @classmethod
    def get(cls, s_id):
        if type(s_id) == int:
            s_id = str(s_id)

        uri = "{url}/{id}".format(url=URL,id=s_id)
        resp = requests.get(uri,headers=cls.__get_headers())
        resp.close()
        return resp.json()

    @classmethod
    def get_field(cls, s_id, field):
        if type(s_id) == int:
            s_id = str(s_id)
            
        uri = "{url}/{id}/fields/{field}".format(url=URL, id=s_id, field=field)
        resp = requests.get(uri, headers=cls.__get_headers())
        resp.close()
        return resp.json()