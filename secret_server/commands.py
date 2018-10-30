# -*- coding: utf-8 -*-
import requests
import json

from os import path
from secret_server.DataProtection import DataProtection
from secret_server.api_response_handler import handle_api_response as handler
from secret_server.config import Config
from requests.compat import urljoin


def uri_builder(endpoint):
    if path.isfile(Config.CLIENT_PATH):
        base_url = json.loads(DataProtection().decrypt(Config.CLIENT_PATH))["endpoint"]
    else:
        base_url = Config.BASE_URL
    base_url += "/api/{}/".format(Config.API_VERSION)
    url = urljoin(base_url, endpoint)
    return url


class AccessToken:

    @classmethod
    def get_token(cls):
        base_url = json.loads(DataProtection().decrypt(Config.CLIENT_PATH))["endpoint"] if \
            path.isfile(Config.CLIENT_PATH) else Config.BASE_URL
        creds = json.loads(DataProtection().decrypt(Config.CREDS_PATH))
        resp = requests.post(base_url+"/oauth2/token", data=creds, verify=False)
        creds = None
        return handler(resp)["access_token"]


class Secret:

    @classmethod
    def __get_headers(cls):
        headers = {
            "Authorization": "bearer {token}".format(token=AccessToken.get_token()),
            "Content-Type": "application/json"
        }
        return headers

    @classmethod
    def get(cls, s_id):
        if type(s_id) == int:
            s_id = str(s_id)

        uri = "{}/{}".format(uri_builder("secrets"), s_id)
        resp = requests.get(uri, headers=cls.__get_headers(), verify=False)
        return handler(resp)

    @classmethod
    def get_field(cls, s_id, field_name):
        # type: (int, str) -> dict
        if type(s_id) == int:
            s_id = str(s_id)

        uri = "{}/{}/fields/{}".format(uri_builder("secrets"), s_id, field_name)
        resp = requests.get(uri, headers=cls.__get_headers(), verify=False)
        return handler(resp)
