from urllib.parse import urlsplit

from flask import current_app, request
from werkzeug.exceptions import NotFound


def route_from(url, method=None):
    environ = dict(request.environ)
    url_request = current_app.request_class(environ)
    url_adapter = current_app.create_url_adapter(url_request)
    parsed_url = urlsplit(url)

    if parsed_url.netloc != "" and parsed_url.netloc != url_adapter.server_name:
        raise NotFound()

    return url_adapter.match(parsed_url.path, method)


# --- start of Flask-RESTful code ---
# Copyright (c) 2013, Twilio, Inc.
# All rights reserved.
# This code is part of Flask-RESTful and is governed by its
# license. Please see the LICENSE file in the root of this package.
def unpack(value):
    """Return a three tuple of data, code, and headers"""
    if not isinstance(value, tuple):
        return value, 200, {}

    try:
        data, code, headers = value
        return data, code, headers
    except ValueError:
        pass

    try:
        data, code = value
        return data, code, {}
    except ValueError:
        pass

    return value, 200, {}


def get_value(key, obj, default):
    if hasattr(obj, '__getitem__'):
        try:
            return obj[key]
        except (IndexError, TypeError, KeyError):
            pass
    return getattr(obj, key, default)
# --- end of Flask-RESTful code ---


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
