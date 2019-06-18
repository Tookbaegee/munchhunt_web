from app.realtime import bp
from app import socketio

from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# authenticate users on connecting

from app.models import User

@bp.route("/test")
def test():
    return render_template("realtime/test.html")

@socketio.on("connect")
def connect():
    print("connect?")
    token = request.args.get("token")
    user = User.check_token(token)
    if token and user:
        emit("response", {"data": "Successfuly authenticated as " + user.username})
    else: 
        emit("response", {"data": "Failed to authenticate."})
        disconnect()
