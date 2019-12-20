from aiohttp import web


def format_header_nginx(h):
    prev_need = True
    h = h.lower().replace('_', '-')
    h2 = ''
    for i in range(len(h)):
        if prev_need:
            h2 += h[i].upper()
            prev_need = False
        else:
            if not h[i].isalpha():
                prev_need = True
            h2 += h[i]
    return h2


def get_raw_request_from_aiohttp_request_summary(request: web.Request) -> str:
    return '{method} {path}'.format(method=request.method, path=request.path)


def get_raw_response_from_aiohttp_response_summary(response: web.Response) -> str:
    return '{status} {reason}'.format(status=response.status, reason=response.reason)


async def get_raw_request_from_aiohttp_request(request: web.Request) -> str:
    headers_str = ''.join(
        ['{}: {}\r\n'.format(format_header_nginx(header), request.headers[header]) for header in request.headers])
    d = await request.read()
    req_built = '{method} {path}{protocol}\r\n' \
                '{headers}\r\n' \
                '{data}'\
        .format(
            method=request.method,
            path=request.rel_url,
            protocol='',
            headers=headers_str,
            data=d.decode() if d and len(d) > 0 else ''
        )
    return req_built
