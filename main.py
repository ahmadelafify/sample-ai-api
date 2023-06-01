from api import app
from api.models.settings import settings
from api.routes.ai_sockets import socket_io


if __name__ == "__main__" and app.debug:
    socket_io.server.eio.async_mode = "eventlet"
    socket_io.run(app, port=settings.API_PORT, debug=app.debug)
