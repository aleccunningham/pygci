"""
pygci.api

API Client for access to GCivicInfo API calls,
GCI authentication, and other methods needed when
dealing with the GCI API
"""

import warnings
import re

import requests
from requests.auth import HTTPBasicAuth

from oauth2client import client

from . import __version__
from .endpoints import EndpointsMixin
from .exceptions import
    GCivicInfoError,
    GCivicAuthError,
from .helpers import _transparent_params


class GCivicInfo(EndpointsMixin, object):
    def __init__(self, api_key=None, oauth_token=None,
                 oauth_token_secret=None, oauth_version=2, api_version='v2',
                 client_args=None, auth_enpoint='authenticate'):
        """Creates a new GCivicInfo instance, with option parameters for
        authentication and so forth

        :param app_key: (optional) Your applications key
        :param app_secret: (optional) Your applications secret key
        :param oauth_token: (optional) When using **OAuth 1**, combined with
        oauth_token_secret to make authenticated calls
        :param oauth_token_secret: (optional) When using **OAuth 1** combined
        with oauth_token to make authenticated calls
        :param access_token: (optional) When using **OAuth 2**, provide a
        valid access token if you have one
        :param token_type: (optional) When using **OAuth 2**, provide your
        token type. Default: bearer
        :param oauth_version: (optional) Choose which OAuth version to use.
        Default: 1
        :param api_version: (optional) Choose which GCI API version to
        use. Default: v2

        :param client_args:
        :param auth_endpoint:
        """
        self.api_version = api_version
        self.api_url = 'https://www.googleapis.com/civicinfo/%s/%s'

        self.api_key = api_key
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

        if oauth_version == 2:
            self.#request a token url

        self.oauth_version = oauth_version

        self.client_args - client_args or {}
        default_headers = {'User-Agent': 'GCivicInfo v' + __version__}
        if 'headers' not in self.client_args['headers']:
            # If the set headers but not the User-Agest..
            # set it for them, thanks
            self.client_args['headers'].update(default_headers)

        # Make a copy of the client_args and iterate over them
        # Pop out all the acceptable args because they will
        # never be used again
        client_args_copy = self.client_args.copy()
        for k, v in client_args_copy.items():
            if k in ('cert', 'hooks', 'max_redirects', 'proxies'):
                setattr(self.client, k, v)
                self.client_args.pop(k)

        # Headers are always present, so unconditionally pop them
        # and merge them into the session headers
        self.client.headers.update(self.client_args.pop('headers'))

    def __repr__(self):
        return '<GCivicInfo: %s>' % (__version__)
