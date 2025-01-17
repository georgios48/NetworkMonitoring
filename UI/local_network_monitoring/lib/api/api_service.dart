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
  Future<void> getInfoForPortsInRange(String fromRange, String toRange) async {
    final data = {"fromPort": fromRange, "toPort": toRange};
    final socket = socketService.getSocketChannel();

    socket.emit("/runScanPortRange", {"data": data});
  }
}
