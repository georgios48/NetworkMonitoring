"""Flask Application"""

from flask import Flask, json
from flask_socketio import SocketIO, emit
from services.new_monitoring import run_scanPortRange

app = Flask(__name__)

# Enable usage of websockets
socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")
socketio.init_app(app)

@socketio.on('/runScanPortRange')
def run_scan_port_range(data):
    """Run Scan Port Range"""

    print(data)

    to_port = data["data"].get("toPort", None)
    from_port = data["data"].get("fromPort", None)

    if to_port is None or from_port is None:
        # TODO: think of a way to break the code here because backend blows
        emit("error", "Invalid port data - 'from port' or 'to port' cannot be empty")

    run_scanPortRange(from_port, to_port, socketio)


# ----- Error Handling ----- #
# TODO: maybe useless because of websockets, they dont return HTTP exception
@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""

    response = e.get_response()

    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

# ----- Socket Consumer ----- #
@socketio.on('connect')
def handle_connect():
    """Handles connecting to WebSocket"""

    print("WebSocket client connected")
    emit('connection', {"connection": "Connected to WebSocket!"})

@socketio.on('disconnect')
def handle_disconnect():
    """Handles disconnecting to WebSocket"""

    print("Disconnection WebSocket client")
    emit('connection', {"connection": "Disconnected from WebSocket!"})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8001)
