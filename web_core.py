import traceback
import logging
import sys
from aiohttp import web
from aiohttp.web import RouteDef

from typing import List, Callable, Optional, Dict, Awaitable

from utils import (
    get_raw_request_from_aiohttp_request_summary,
    get_raw_response_from_aiohttp_response_summary
)


class WebCore:
    """"""
    def __init__(self):
        self._logger = self._create_default_logger()

        self._application = web.Application(middlewares=[self._handle_request], logger=self._logger)

    def mount_routes(
            self,
            root: str,
            routes: List[RouteDef],
            middlewares=None
    ):
        """
        Each route will be mounted at the location /<root>/<route>

        :param root: Root to mount the routes at.
        :param routes: List of handlers.
        :param middlewares: List of middlewares decorated by web.middleware
        """
        app = web.Application(middlewares=middlewares)
        app.add_routes(routes)
        self._application.add_subapp(prefix=root, subapp=app)

    @web.middleware
    async def _handle_request(
            self,
            request: web.Request,
            handler: BaseRouteHandlerType
    ) -> web.Response:
        """
        All requests go through this middleware

        Note! From aiohttp doc

            Warning
            Second argument should be named handler exactly.

        Exceptions can escape here. If they come from web.HTTP_ then aiohttp will send the appropriate response,
        otherwise a 500 error is sent.

        The core handles various data that are appended to the request

        'cloud' -> self
        'exception' -> stores exception if exception was captured. May be unpopulated.
        'no_log' -> if populated (any value), then no logging will occur.

        :param request: Web request
        :param handler: Function taking a (re
        :return:
        """
        request['cloud'] = self

        response = None
        try:
            response = await handler(request)
        except web.HTTPException as exc:
            response = exc
        except Exception as exc:
            response = web.HTTPInternalServerError()
        finally:
            if not isinstance(response, web.StreamResponse):
                response = web.HTTPInternalServerError()
            await response.prepare(request)

        return response

