from enum import Enum
from typing import TypeVar, Generic, Callable, Dict

import requests

from rest_resources.api_object import ApiObject

_RootResource = TypeVar('_RootResource', bound=ApiObject)


class AuthHeader(dict):
    @classmethod
    def bearer(cls, token: str) -> Dict[str, str]:
        return cls(Authorization=f'bearer {token}')

    @classmethod
    def basic(cls, token: str) -> Dict[str, str]:
        return cls(Authorization=f'basic {token}')


_AuthImplementation = Callable[[], AuthHeader]


class Verb(Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


GET = Verb.GET
PUT = Verb.PUT
POST = Verb.POST
PATCH = Verb.PATCH
DELETE = Verb.GET


class ResourceClient(Generic[_RootResource]):
    _resource: _RootResource
    _session: requests.session
    _auth: _AuthImplementation

