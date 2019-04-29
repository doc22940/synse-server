"""Error definitions for Synse Server."""

from sanic.handlers import ErrorHandler

from synse_server.i18n import _
from synse_server.utils import rfc3339now, http_json_response


class SynseErrorHandler(ErrorHandler):
    """A custom error handler for Synse Server to be used by the underlying
    Sanic application.

    This error handler will ensure that SynseErrors which are raised will be
    returned with response JSON.
    """

    def default(self, request, exception):
        """The default error handler for exceptions.

        This handles errors which have no error handler assigned. Synse Server
        does not register any other custom error handlers, so all exceptions
        raised by the application will be caught and handled here.
        """
        if issubclass(type(exception), SynseError):
            return http_json_response(
                body=exception.make_response(),
                status=exception.http_code,
            )
        else:
            return super(SynseErrorHandler, self).default(request, exception)


class SynseError(Exception):
    """The base exception class for all errors raised by Synse Server."""

    # The default HTTP code for Synse Server errors is 500 (server error).
    # Subclassed errors should override this to use a different response code.
    http_code = 500

    # The short description for the error. This is returned in the response
    # body JSON under the 'description' field. Each subclassed error should
    # override this with their own error-specific description.
    description = 'an unexpected error occurred'

    def make_response(self):
        """Make a JSON error response from the Synse Error.

        Returns:
            dict: A dictionary representation of the error response.
        """
        return {
            'http_code': self.http_code,
            'description': self.description,
            'timestamp': rfc3339now(),
            'context': str(self),
        }


class InvalidUsage(SynseError):
    """The request contained invalid input.

    This occurs when a user provides bad input, such as a bad URI parameter,
    query parameter, or an invalid JSON body.
    """

    http_code = 400
    description = _('invalid user input')


class NotFound(SynseError):
    """The requested resource was not found.

    This occurs when the ID provided for a resource does not resolve to any
    known entity. This can be due to things like cache invalidation, plugin
    failure, typos in the requested ID, etc.
    """

    http_code = 404
    description = _('resource not found')


class UnsupportedAction(SynseError):
    """The requested action is not supported by the specified device.

    This occurs when an action (read/write) is requested on a device which
    does not support that action. A device's action support is determined
    at the plugin level.
    """

    http_code = 405
    description = _('device action not supported')


class ServerError(SynseError):
    """The request failed for a non-specific reason.

    This occurs when there is a non-specific error when attempting to fulfill
    a request. It can be used as the error type for cases which do not fit any
    of the other request errors.
    """

    http_code = 500
    description = _('error processing the request')