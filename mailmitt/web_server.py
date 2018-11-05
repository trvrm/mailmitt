"""
    I'd rather use web.RouteTableDef, but that's a very recent addition 
    to aiohttp that isn't supported on python3.5 as far as I can tell.
    
"""
from . import smtp_server

from aiohttp import web
import pathlib
import functools
from .utils import dumps


import bottle

# This is the only thing we use from Bottle - its excellent lightweight templating engine.
from bottle import template

HERE = pathlib.Path(__file__).absolute().parent

bottle.TEMPLATE_PATH = [str(HERE / "templates")]

json_response = functools.partial(web.json_response, dumps=dumps)


def get_part_by_type(message, type_):
    for part in message["parts"]:
        if part["type"] == type_:
            return part["body"]


app = web.Application()


async def index(request):
    index = request.query.get("index")
    message = None
    if index is not None:
        index = int(index)
        message = (
            smtp_server.messages[index] if index < len(smtp_server.messages) else None
        )

    text = template(
        "index",
        {
            "messages": smtp_server.messages,
            "message": message,
            "dumps": dumps,
            "index": index,
        },
    )
    return web.Response(text=text, content_type="text/html")


async def clear(request):
    smtp_server.messages.clear()
    return web.HTTPFound("/")


async def message_source(request):
    index = int(request.match_info["index"])
    message = smtp_server.messages[index]
    return web.Response(text=message["source"])


async def message_plain(request):
    index = int(request.match_info["index"])
    message = smtp_server.messages[index]
    print(message)
    text = get_part_by_type(message, "text/plain") or ""
    text = text.replace("\r\n", "\n")  # aiosmtpd seems to put these in.
    return web.Response(text=text, content_type="text/plain")


async def message_html(request):
    index = int(request.match_info["index"])
    message = smtp_server.messages[index]
    text = get_part_by_type(message, "text/html") or ""
    return web.Response(text=text, content_type="text/html")


def indexify(message, index):
    return {
        "id": index,
        "formats": {
            "source": "/messages/{}.source".format(index),
            "plain": "/messages/{}.plain".format(index),
        },
        **message,
    }


async def message_json(request):
    index = int(request.match_info["index"])
    message = smtp_server.messages[index]

    return json_response(indexify(message, index))


def get_messages(request):
    return json_response(
        {
            "messages": [
                indexify(message, index)
                for index, message in enumerate(smtp_server.messages)
            ]
        }
    )


app.router.add_get("/", index)
app.router.add_get("/clear", clear)
app.router.add_get("/messages/{index}.source", message_source)
app.router.add_get("/messages/{index}.plain", message_plain)
app.router.add_get("/messages/{index}.html", message_html)
app.router.add_get("/messages/{index}.json", message_json)
app.router.add_get("/messages", get_messages)
app.router.add_delete("/messages", clear)
app.router.add_static("/static/", path=HERE / "static", name="static")
