# -*- coding: utf-8 -*-


class JellyfinApiException(Exception):
    """ Base class for all JellyfinAPI exceptions. """
    pass


class BadRequest(JellyfinApiException):
    """ An invalid request, generally a user error. """
    pass


class NotFound(JellyfinApiException):
    """ Request media item or device is not found. """
    pass


class UnknownType(JellyfinApiException):
    """ Unknown library type. """
    pass


class Unsupported(JellyfinApiException):
    """ Unsupported client request. """
    pass


class Unauthorized(BadRequest):
    """ Invalid username/password or token. """
    pass


class TwoFactorRequired(Unauthorized):
    """ Two factor authentication required. """
    pass
