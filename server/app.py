from flask import Flask, render_template, request
from flask_socketio import SocketIO
from global_variable import socketid_client
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins="*")


@app.route("/")
def hello_world():
    return "Hello World"


@socketio.on('connect')
def handle_message():
    print('user has connected. your id is', request.sid)


@socketio.on('login')
def handle_my_custom_event(json):
    global socketid_client
    user_id = json.get("user_id")
    sid = request.sid
    socketid_client.append({"user_id": user_id, "sid": sid})
    print("List client login", socketid_client)


@socketio.on("change_privilege")
def handle_event_change_privilege(json):
    global socketid_client
    print(json)
    user_id_change = json.get("user_id", 0)
    sid = None
    for item in socketid_client:
        if item["user_id"] == user_id_change:
            sid = item["sid"]
    socketio.emit("require_logout",
                  {"message": "Hey you need to logout"},
                  room=sid)


@socketio.on('disconnect')
def handle_event_disconnect():
    """
    handle event disconnect
    """
    global socketid_client
    print("disconnect success")
    sid_delete = request.sid
    for index, item in enumerate(socketid_client):
        if item["sid"] == sid_delete:
            del socketid_client[index]
    print("handle_event_disconnect", socketid_client)


if __name__ == '__main__':
    socketio.run(app, debug=True)
