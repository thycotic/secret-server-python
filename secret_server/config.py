# -*- coding: utf-8 -*-
import requests
import json

from os import (environ, path, remove)
from platform import (system, _sys_version, node)
from uuid import uuid4
from secret_server.DataProtection import DataProtection


class Config:
    # These are the arguments required to create a client in Secret Server
    CLIENT_CONFIG = {
        "clientId": uuid4(),
        "description": "Machine: {node}, OS: {system} - Python {version}".format(node=node(), system=system(), version=_sys_version()[1]),
        "name": node(),
        "ruleName": '' or environ.get("RULE_NAME"),
        "onboardingKey": '' or environ.get("RULE_KEY")
    }

    BASE_URL = '' or str(environ.get("SECRET_SERVER_BASE_URL")).rstrip("/")

    CREDS_PATH = "creds.json"
    CLIENT_PATH = "client_info.json"
    API_VERSION = "v1"
    SSL_VERIFY = False

    __encrypt = DataProtection().encrypt
    __decrypt = DataProtection().decrypt

    @classmethod
    def register_client(cls):
        if not path.exists(cls.CREDS_PATH):
            resp = requests.post(cls.BASE_URL+"/api/v1/sdk-client-accounts", data=cls.CLIENT_CONFIG, verify=False)
            # The SDK accounts support client credentials grant type. We generate the clientID in our Python client
            # and Secret Server generates the ClientSecret
            creds = {
                "client_id": "sdk-client-"+resp.json()["clientId"],
                "client_secret": resp.json()["clientSecret"],
                "grant_type": "client_credentials"
            }
            # In order to easily consume the credentials by the requests package, we use
            # json.dumps before we encrypt the data
            creds = cls.__encrypt(json.dumps(creds))
            try:
                open(cls.CREDS_PATH, "w").write(creds)
            except IOError as e:
                raise IOError("Couldn't Save credentials: ", e)

            config = {
                "id": resp.json()["id"],
                "endpoint": cls.BASE_URL
            }
            config = cls.__encrypt(json.dumps(config))
            try:
                open(cls.CLIENT_PATH, "w").write(config)
            except IOError as e:
                raise IOError("Couldn't Save client info: ", e)

            resp.close()
            print("Client Registered")
        else:
            print("client already registered")
    
    @classmethod
    def remove_client(cls, revoke):
        # This method removes the client configuration from disk. There is an optional revoke param which removes the
        # client from secret server as well
        if path.exists(cls.CLIENT_PATH):
            if revoke:
                import secret_server.commands as commands
                token = commands.AccessToken.get_token()
                client_id = json.loads(cls.__decrypt(cls.CLIENT_PATH))["id"]
                base_url = json.loads(DataProtection().decrypt(Config.CLIENT_PATH))["endpoint"] if \
                    path.isfile(Config.CLIENT_PATH) else Config.BASE_URL
                resp = requests.post(
                    "{base_url}/api/v1/sdk-client-accounts/{client_id}/revoke".format(base_url=base_url,
                    client_id=client_id),
                    headers={"Authorization": "bearer {token}".format(token=token)},
                    verify=False
                )

                if resp.status_code is not 200:
                    print(resp.json()["body"])
                    
                resp.close()
            remove(cls.CLIENT_PATH)
            remove(cls.CREDS_PATH)
            DataProtection.remove_master_key()
            print("Client unregistered")
        else:
            print("Client already unregistered")
