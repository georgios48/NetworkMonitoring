"""Flask Application"""

from flask import Flask, json, request
from flask_socketio import SocketIO, emit
from services.new_monitoring import get_device_info, run_scanPortRange

app = Flask(__name__)

# Enable usage of websockets
socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")
socketio.init_app(app)

# ---- Helper Functions ----- #
def is_any_none(*args):
    """Checks if any of the element is none"""

    return any(arg is None for arg in args)

# ----- Endpoints ----- #
@socketio.on('/runScanPortRange')
def run_scan_port_range(data):
    """Run Scan Port Range"""

    to_port = data["data"].get("toPort", None)
    from_port = data["data"].get("fromPort", None)

    if is_any_none(to_port, from_port):
        emit("error", "Invalid port data - 'from port' or 'to port' cannot be empty")
    else:
        run_scanPortRange(from_port, to_port, socketio)

@app.route("/displayDeviceInfo", methods=["POST"])
def display_device_info(data):
    """Displays info for the device"""

    oid = data["data"].get("oid", None)
    ip_target = data["data"].get("ipTarget", None)
    community = data["community"].get("community", None)

    if is_any_none(oid, ip_target, community):
        emit("error", "Invalid oID, IP or community")
    else:
        get_device_info(oid, ip_target, community, socketio)

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
