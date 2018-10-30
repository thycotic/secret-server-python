# -*- coding: utf-8 -*-
from secret_server.config import Config
from secret_server.commands import get_token
from secret_server.commands import Secret


class SdkClient:
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls.__singleton:
            cls.__singleton = object.__new__(SdkClient)
        return cls.__singleton

    def __init__(self):
        self.token = get_token
        self.ssl_verify = Config.SSL_VERIFY

    @classmethod
    def configure(cls, **kwargs):
        """
        Configures the client connection to Secret Server. If no values are provided then it will look for
        environment variables

        :param dict | str kwargs: Key/Value pairs to register the client see below
        :keyword str url: The Secret Server Url
        :keyword str rule: The Rule Name
        :keyword str key: The generated rule key

        """
        if kwargs:
            Config.BASE_URL = str(kwargs['url']).rstrip("/")
            Config.CLIENT_CONFIG['ruleName'] = kwargs['rule']
            if "key" in kwargs:
                Config.CLIENT_CONFIG['onboardingKey'] = kwargs['key']

        Config.register_client()
    
    @classmethod
    def remove(cls, revoke=False):
        # type: (bool) -> None
        """
        Removes the client configuration from the machine with optional revocation

        :param bool revoke: True/False to revoke client in Secret Server. Default is False
        """
        try:
            Config.remove_client(revoke)
        except Exception:
            raise
    
    @classmethod
    def get_secret(cls, s_id):
        # type: (int) -> dict
        """
        Retrieves a Secret by Id and returns a secret object

        :param int s_id: The Secret Id
        :return: Secret object (dict)
        """
        return dict(Secret.get(s_id))

    @classmethod
    def get_secret_field(cls, s_id, field):
        # type: (int, str) -> str
        """
        Retrieves a Secret by Id and field slug (name) and returns a string

        :param int s_id: The Secret Id
        :param str field: The field slug
        :return: str
        """
        return str(Secret.get_field(s_id, field))
