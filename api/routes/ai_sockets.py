from flask import request
from flask_socketio import SocketIO, send, emit
from flask_sock import Sock
from simple_websocket import Server as WebsocketServer

from api import app
from api.utils.openai import get_openai_response


socket_io = SocketIO(app, path="/socket")
websockets = Sock(app)


@websockets.route('/websocket/talk')
def talk_websocket(ws: WebsocketServer):
    print(f"""Talking connection started
    Client IP: {request.remote_addr}""")
    while True:
        message = ws.receive()
        print('Received message:', message)
        ws.send('Response message')


@socket_io.on('connect', namespace="/talk")
def begin_talking():
    print(f"""Talking connection started
    Client IP: {request.remote_addr}
    Client Connection Id: {request.sid}""")


@socket_io.on('json', namespace="/talk")
def talk_json(*args: dict):
    print('Received JSON data:', *args)
    data = args[0]
    if not isinstance(data, dict):
        send({"error": "Message data is not JSON"}, json=True)
        return

    prompt = data.get("data")
    if prompt is None:
        send({"error": "Prompt invalid"}, json=True)
        return
    elif prompt == "Ping":
        response = "Pong"
    else:
        response = get_openai_response(prompt)
    send({"response": response}, json=True)


@socket_io.on('message', namespace="/talk")
def talk_message(*data: dict):
    print('Received message data:', *data)
    message = data[0]
    if not isinstance(message, str):
        send("Message is not plain text")
        return
    elif not message:
        send("Message is empty")
        return

    if message == "Ping":
        response = "Pong"
    else:
        response = get_openai_response(message)
    emit('message', response)


@socket_io.on('disconnect', namespace="/talk")
def stop_talking():
    print(f"""Talking connection stopped
    Client IP: {request.remote_addr}
    Client Connection Id: {request.sid}""")
