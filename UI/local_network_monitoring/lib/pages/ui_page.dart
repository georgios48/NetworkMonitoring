import 'package:flutter/material.dart';
import 'package:local_network_monitoring/api/api_service.dart';
import 'package:local_network_monitoring/models/port_scan.dart';
import 'package:local_network_monitoring/models/process_dto.dart';
import "package:local_network_monitoring/pages/utils/helper_widgets.dart";
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:window_manager/window_manager.dart';

class UiPage extends StatefulWidget {
  const UiPage({super.key});

  @override
  State<UiPage> createState() => _UiPageState();
}

class _UiPageState extends State<UiPage> {
  late IO.Socket channel;
  List<dynamic> bigTerminalMessages = [];
  List<PortScanModel> smallTerminalMessages = [];

  // Text Controllers
  final TextEditingController ipSelectionController = TextEditingController();
  final TextEditingController oIDSelectionController = TextEditingController();
  final TextEditingController communitySelectionController =
      TextEditingController();

  @override
  @override
  void initState() {
    // Handshake with a WebSocket
    SocketService socketService = SocketService();
    socketService.initializeWebSocket();
    channel = socketService.getSocketChannel();

    // Configure WebSocket listeners, to listen on changes so they can update the variables responsible for the UI
    _adjustListeners();

    super.initState();
  }

  void _adjustListeners() {
    // Scan port range listener
    channel.on(
      "runScanPortRange",
      (data) {
        // Update the list of messages
        PortScanModel portScanModel = PortScanModel.fromJson(data);

        setState(() {
          bigTerminalMessages.add(portScanModel);
        });
      },
    );

    // Listen for process info
    channel.on("process", (process) {
      // Update terminal messages
      ProcessDTO processModel = ProcessDTO.fromJson(process);

      setState(() {
        bigTerminalMessages.add(processModel);
      });
    });

    // Errors listener
    channel.on(
      "error",
      (data) {
        // TODO: map the data to a DTO object and append it to a variable or something,
        // which will be listened by a provider and update the UI if needed
        print(data);
      },
    );
  }

  @override
  void dispose() {
    channel.disconnect();
    channel.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    //! By double clicking, return the window into original position

    return GestureDetector(
      onDoubleTap: () {
        moveWindowToCenter();
      },
      child: SafeArea(
        child: Scaffold(
          body: Padding(
            padding: const EdgeInsets.fromLTRB(30, 30, 30, 5),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Change theme button
                ThemeButton(),

                SizedBox(height: 20),

                // IP address selection and OID selection
                Row(
                  children: [
                    Expanded(
                      child: Align(
                        alignment: Alignment.centerLeft,
                        child: IpSelection(
                          controller: ipSelectionController,
                        ),
                      ),
                    ),

                    Expanded(
                      child: Align(
                        alignment: Alignment.center,
                        child: OIdSelection(
                          controller: oIDSelectionController,
                        ),
                      ),
                    ),

                    // Scan all devices button
                    Expanded(
                      child: Align(
                        alignment: Alignment.centerRight,
                        child: InfoForDeviceButton(),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 20),

                // Community and Stop Scan button
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Expanded(
                      child: Align(
                        alignment: Alignment.centerLeft,
                        child: CommunitySelection(
                          controller: communitySelectionController,
                        ),
                      ),
                    ),

                    // LinearProgressIndicator(
                    //   value: 0.5,
                    //   backgroundColor: Colors.grey,
                    // ),

                    // Stop scan button
                    Expanded(
                      child: Align(
                        alignment: Alignment.centerRight,
                        child: StopScanningButton(),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 20),

                // Scan range of ports
                ScanningPortsElements(),

                const SizedBox(height: 20),

                // Allow/Forbid Port
                AllowForbitPortElements(),

                const SizedBox(height: 10),

                // Terminal
                Expanded(
                  flex: 1,
                  child: Row(
                    children: [
                      TerminalWidget(
                        flexSpaceToTake: 2,
                        terminalMessages: bigTerminalMessages,
                      ),
                      const SizedBox(width: 5),
                      Expanded(
                          child: TerminalWidget(
                        flexSpaceToTake: 1,
                        terminalMessages: smallTerminalMessages,
                      ))
                    ],
                  ),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }

  // Move the window to the center of the screen
  void moveWindowToCenter() async {
    await windowManager.center();
  }
}
