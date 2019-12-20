import traceback
import os
from aiohttp import web

from utils import (
    get_raw_request_from_aiohttp_request,
    get_raw_request_from_aiohttp_request_summary,
    get_raw_response_from_aiohttp_response_summary
)


async def serve(request: web.Request) -> web.Response:
    requested_file = request.match_info['path']

    if len(requested_file) == 0:
        return web.HTTPFound('/index.html')

    requested_file = os.path.abspath(os.path.join('.', requested_file))

    if requested_file.find('..') >= 0:
        return web.HTTPForbidden()

    if not os.path.exists(requested_file):
        return web.HTTPNotFound()

    content_type = 'text/html'
    if requested_file.endswith('css'):
        content_type = 'text/css'
    elif requested_file.endswith('js'):
        content_type = 'text/javascript'
    with open(requested_file, 'r') as page:
        return web.Response(text=page.read(), content_type=content_type)


@web.middleware
async def logging_middleware(
        request: web.Request,
        handler
) -> web.Response:
    response = web.HTTPInternalServerError(text='Unknown Error.')

    print(await get_raw_request_from_aiohttp_request(request))
    try:
        response = await handler(request)
    except:
        response = web.HTTPInternalServerError(text=traceback.format_exc())
    finally:
        print(get_raw_response_from_aiohttp_response_summary(response))

    return response


async def initialize() -> web.Application:
    app = web.Application(middlewares=[logging_middleware], logger=None)

    routes = [
        web.get(r'/{path:.*}', serve),
    ]
    app.add_routes(routes)

    return app


if __name__ == '__main__':
    web.run_app(
        initialize(),
        host='127.0.0.1',
        port=8080,
    )
