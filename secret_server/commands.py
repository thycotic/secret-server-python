# -*- coding: utf-8 -*-
import requests
import json
import os

from secret_server.data_protection import DataProtection
from secret_server.api_response_handler import HandleApiResponse as handler
from secret_server.config import Config

class AccessToken:

    @classmethod
    def get_token(cls):
        BASE_URL = DataProtection().decrypt(Config.CLIENT_PATH)["endpoint"] if os.path.exists(Config.CLIENT_PATH) else Config.BASE_URL
        creds = DataProtection().decrypt(Config.CREDS_PATH)
        resp = requests.post(BASE_URL+"/oauth2/token", data=creds, verify=False)
        creds = None
        return handler(resp)["access_token"]

class Secret:

    @classmethod
    def __get_headers(cls):
        headers = {"Authorization" : "bearer {token}".format(token=AccessToken.get_token()), "Content-Type" : "application/json"}
        return headers

    @classmethod
    def get(cls, s_id):
        if type(s_id) == int:
            s_id = str(s_id)
        BASE_URL = DataProtection().decrypt(Config.CLIENT_PATH)["endpoint"] if os.path.exists(Config.CLIENT_PATH) else Config.BASE_URL or Config.BASE_URL
        URL = "{base_url}/api/v1/secrets".format(base_url=BASE_URL)
        uri = "{url}/{id}".format(url=URL,id=s_id)
        resp = requests.get(uri,headers=cls.__get_headers(), verify=False)
        return handler(resp)

    @classmethod
    def get_field(cls, s_id, field):
        if type(s_id) == int:
            s_id = str(s_id)
        BASE_URL = DataProtection().decrypt(Config.CLIENT_PATH)["endpoint"] if os.path.exists(Config.CLIENT_PATH) else Config.BASE_URL or Config.BASE_URL
        URL = "{base_url}/api/v1/secrets".format(base_url=BASE_URL)
        uri = "{url}/{id}/fields/{field}".format(url=URL, id=s_id, field=field)
        resp = requests.get(uri, headers=cls.__get_headers(), verify=False)
        return handler(resp)