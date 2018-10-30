# -*- coding: utf-8 -*-
from secret_server.config import Config
from secret_server.commands import AccessToken
from secret_server.commands import Secret


class SdkClient:
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls.__singleton:
            cls.__singleton = object.__new__(SdkClient)
        return cls.__singleton

    def __init__(self):
        self.token = AccessToken.get_token
        self.ssl_verify = Config.SSL_VERIFY

    @classmethod
    def configure(cls, **kwargs):
        """
Configures and registers the client in Secret Server. This method takes a key word args for url, rule, and key or a dict
object.
configure(url="https://youre-ss-url",rule="rule-name", key="rule-key")
        """
        if kwargs:
            Config.BASE_URL = str(kwargs['url']).rstrip("/")
            Config.CLIENT_CONFIG['ruleName'] = kwargs['rule']
            Config.CLIENT_CONFIG['onboardingKey'] = kwargs['key']

        Config.register_client()
    
    @classmethod
    def remove(cls, revoke=False):
        # type: (*bool) -> None
        """
        Removes the clients configuration and stored credentials. By default this doesn't revoke the client in Secret
        Server
        """
        Config.remove_client(revoke)
    
    @classmethod
    def get_secret(cls, s_id):
        # type: (int) -> dict
        """This methods gets a Secret by ID (s_id)"""
        return dict(Secret.get(s_id))

    @classmethod
    def get_secret_field(cls, s_id, field):
        # type: (int, str) -> str
        """This methods gets a Secret field by ID(s_id) and field Slug"""
        return str(Secret.get_field(s_id, field))
