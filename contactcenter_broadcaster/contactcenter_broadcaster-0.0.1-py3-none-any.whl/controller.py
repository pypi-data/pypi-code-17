from asyncio import ensure_future
from aiohttp.web import Response
from multidict import MultiDict
from uuid import uuid4
from concurrent.futures import CancelledError, TimeoutError

from .websocket import WebSocketResponse
from .asterisk import WSMsgDispatcher
from . import service
from .logger import controller as log


async def ami(request):

    ip, _ = request.transport.get_extra_info('peername')
    socket = await WebSocketResponse.instance(request)
    dispatcher = WSMsgDispatcher(socket, ip)

    log.info(f"new WS connection from: {ip} with hash {socket.hash} - ({dispatcher.len})")

    try:
        async for msg in socket:
            ensure_future(dispatcher.dispatch(msg))

    except (ValueError, TimeoutError, CancelledError) as error:
        log.error(error)
    finally:
        dispatcher.exit()
        log.info(f"close connection for {ip} - ({dispatcher.len})")

    return socket


class Xml:
    _api = service.OutboundXls()

    @classmethod
    async def slice_report(cls, request):

        return Response(
            body=await cls._api.asxls(
                request.GET.getone('begin', None),
                request.GET.getone('end', None)
            ),
            headers=MultiDict({
                "Content-Type": "application/vnd.ms-excel",
                "Content-Disposition": f"attachment; filename=\"SliceXslReport.{uuid4()!s}.xls\""
            })
        )


routes = (
    ("/ami", ami),
    ("/report/outbound/slice/xsl", Xml.slice_report)
)
