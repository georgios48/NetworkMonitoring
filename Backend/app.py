# pylint: disable=import-error
"""Flask Application"""

from flask import Flask
from flask_socketio import SocketIO, emit
from services.network_monitoring import (disable_port, enable_port,
                                         get_device_info,
                                         perform_port_range_scan, stop)

app = Flask(__name__)

# Enable usage of websockets
socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")
socketio.init_app(app)

# ---- Helper Functions ----- #
def is_any_none(*args):
    """Checks if any of the element is none"""

    return any(arg is None or arg == "" for arg in args)

# ----- Endpoints ----- #
@socketio.on('/runScanPortRange')
def run_scan_port_range(data):
    """Run Scan Port Range"""

    to_port = data["data"].get("toPort", None)
    from_port = data["data"].get("fromPort", None)
    ip_target = data["data"].get("ipTarget", None)
    community = data["data"].get("community", None)

    if is_any_none(to_port, from_port):
        emit("error", {"bigTerminalError": "Invalid port data - 'from port' or 'to port' cannot be empty"})
    else:
        perform_port_range_scan(from_port, to_port, ip_target, community, socketio)

@socketio.on("/displayDeviceInfo")
def display_device_info(data):
    """Displays info for the device"""

    oid = data["data"].get("oid", None)
    ip_target = data["data"].get("ipTarget", None)
    community = data["data"].get("community", None)

    if is_any_none(oid, ip_target, community):
        emit("error", {"bigTerminalError": "Invalid oID, IP or community"})
    else:
        get_device_info(oid, ip_target, community, socketio)

@socketio.on("/forceStop")
def stop_process():
    """Stop executing process"""

    stop(socketio)

@socketio.on("/enablePort")
def enable_snmp_port(data):
    """Enable port"""

    ip_target = data["data"].get("ipTarget", None)
    community = data["data"].get("community", None)
    port_to_enable = data["data"].get("portToEnable", None)

    if is_any_none(ip_target, community, port_to_enable):
        emit("error", {"smallTerminalError": "Invalid IP, community or portToEnable"})
    else:
        enable_port(socketio, ip_target, community, port_to_enable)

@socketio.on("/disablePort")
def disable_snmp_port(data):
    """Disable port"""

    ip_target = data["data"].get("ipTarget", None)
    community = data["data"].get("community", None)
    port_to_disable = data["data"].get("portToDisable", None)

    if is_any_none(ip_target, community, port_to_disable):
        emit("error", {"smallTerminalError": "Invalid IP, community or portToDisable"})
    else:
        disable_port(socketio, ip_target, community, port_to_disable)

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
