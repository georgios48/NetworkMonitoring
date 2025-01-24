import 'package:shared_preferences/shared_preferences.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;

class SocketService {
  static final SocketService _instance = SocketService._internal();

  factory SocketService() {
    return _instance;
  }

  SocketService._internal();

  late IO.Socket socket;
  bool _isInitialized = false;

  void initializeWebSocket() {
    if (!_isInitialized) {
      socket = IO.io(
          "ws://127.0.0.1:8001",
          IO.OptionBuilder()
              .setTransports(["websocket"])
              .enableAutoConnect()
              .build());
      _isInitialized = true;
    }
  }

  IO.Socket getSocketChannel() {
    return socket;
  }
}

class ApiService {
  final SocketService socketService = SocketService();

  ApiService() {
    // Init socket
    socketService.initializeWebSocket();
  }

  // Get info for ports scanned in given range
  Future<void> getInfoForPortsInRange(
      String fromRange, String toRange, String ip, String community) async {
    final data = {
      "fromPort": fromRange.trim(),
      "toPort": toRange.trim(),
      "ipTarget": ip.trim(),
      "community": community.trim()
    };
    final socket = socketService.getSocketChannel();

    socket.emit("/runScanPortRange", {"data": data});
  }

  // Get Device info
  Future<void> getDeviceInfo(String ip, String oid, String community) async {
    final data = {
      "ipTarget": ip.trim(),
      "oid": oid.trim(),
      "community": community.trim()
    };
    final socket = socketService.getSocketChannel();

    socket.emit("/displayDeviceInfo", {"data": data});
  }

  // Stop process
  Future<void> stopRunningProcess() async {
    final socket = socketService.getSocketChannel();

    socket.emit("/forceStop");
  }

  Future<void> clearAllSharedPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }
}
