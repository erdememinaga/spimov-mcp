"""HTTP transport — runs as a long-lived service (e.g. mcp.spimov.com).

Exposes two endpoints over the same hosted server:
- POST/GET ``/mcp``  — Streamable HTTP (the current MCP transport; what
  claude.ai custom connectors and recent clients use).
- GET ``/sse`` + POST ``/messages/`` — legacy SSE transport, kept for older
  clients.

Each request carries a Spimov API key, taken from either::

    Authorization: Bearer spk_live_XXXX

or, for connector UIs that only let you enter a URL, the ``?api_key=`` query
param. The key is forwarded to the underlying REST API as-is.

The hosted server hides filesystem-bound tools (create_dub) — a local
file_path can't be honored on a remote transport.
"""
from __future__ import annotations

import contextlib
import contextvars
import os
from urllib.parse import parse_qs

import uvicorn
from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route

from .server import build_server


_active_key: contextvars.ContextVar[str] = contextvars.ContextVar("spimov_api_key", default="")


def _extract_key(request: Request) -> str:
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    # Fallback: ?api_key=... query param (handy for clients that only take a URL)
    return request.query_params.get("api_key", "").strip()


def _extract_key_from_scope(scope) -> str:
    for k, v in scope.get("headers", []):
        if k == b"authorization":
            auth = v.decode("latin-1")
            if auth.lower().startswith("bearer "):
                return auth.split(" ", 1)[1].strip()
    qs = scope.get("query_string", b"").decode("latin-1")
    return parse_qs(qs).get("api_key", [""])[0].strip()


async def _send_401(send) -> None:
    await send({
        "type": "http.response.start",
        "status": 401,
        "headers": [(b"content-type", b"application/json")],
    })
    await send({"type": "http.response.body", "body": b'{"error":"missing_api_key"}'})


def make_app() -> Starlette:
    # One hosted server, shared by both transports; local-only tools hidden.
    server = build_server(get_api_key=lambda: _active_key.get(), include_local=False)

    # --- Streamable HTTP (/mcp) ---------------------------------------------
    # stateless=True so each request is handled inline: the api_key we set on
    # the contextvar before handle_request() propagates into the tool call
    # (a per-session task, as in stateful mode, would not see it).
    session_manager = StreamableHTTPSessionManager(
        app=server,
        event_store=None,
        json_response=True,
        stateless=True,
    )

    async def handle_streamable_http(scope, receive, send) -> None:
        token = _extract_key_from_scope(scope)
        if not token:
            await _send_401(send)
            return
        ctx_token = _active_key.set(token)
        try:
            await session_manager.handle_request(scope, receive, send)
        finally:
            _active_key.reset(ctx_token)

    # --- Legacy SSE (/sse + /messages/) -------------------------------------
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> Response:
        token = _extract_key(request)
        if not token:
            return JSONResponse({"error": "missing_api_key"}, status_code=401)
        ctx_token = _active_key.set(token)
        try:
            async with sse.connect_sse(request.scope, request.receive, request._send) as (read, write):
                await server.run(read, write, server.create_initialization_options())
        finally:
            _active_key.reset(ctx_token)
        return Response()

    async def healthz(_: Request) -> Response:
        return JSONResponse({"status": "ok"})

    @contextlib.asynccontextmanager
    async def lifespan(_: Starlette):
        async with session_manager.run():
            yield

    # Streamable HTTP is mounted at /mcp. A bare POST to /mcp 307-redirects to
    # /mcp/ (Starlette default); 307 preserves the method+body, so clients that
    # connect to either /mcp or /mcp/ work.
    return Starlette(
        debug=False,
        lifespan=lifespan,
        routes=[
            Route("/healthz", endpoint=healthz),
            Mount("/mcp", app=handle_streamable_http),
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )


def main() -> None:
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", "8001"))
    uvicorn.run(make_app(), host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
