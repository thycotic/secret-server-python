# -*- coding: utf-8 -*-
import requests

from secret_server.api_response_handler import handle_api_response as handler
from secret_server.config import Config
from requests.compat import urljoin


def uri_builder(resource_path):
    base_url = Config.load_endpoint() + "/api/{}/".format(Config.API_VERSION)
    url = urljoin(base_url, resource_path)
    return url


def get_token():
    resp = requests.post(Config.load_endpoint()+"/oauth2/token", data=Config.load_credentials(), verify=False)
    return handler(resp)["access_token"]


class Secret:

    @classmethod
    def __get_headers(cls):
        headers = {
            "Authorization": "bearer {token}".format(token=get_token()),
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
        if type(s_id) == int:
            s_id = str(s_id)

        uri = "{}/{}/fields/{}".format(uri_builder("secrets"), s_id, field_name)
        resp = requests.get(uri, headers=cls.__get_headers(), verify=False)
        return handler(resp)
