import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:local_network_monitoring/api/api_service.dart';
import 'package:local_network_monitoring/models/device_info.dart';
import 'package:local_network_monitoring/models/port_scan.dart';
import 'package:local_network_monitoring/models/process_dto.dart';
import "package:local_network_monitoring/pages/utils/helper_widgets.dart";
import 'package:local_network_monitoring/providers/community_cubit.dart';
import 'package:local_network_monitoring/providers/ip_cubit.dart';
import 'package:local_network_monitoring/providers/oid_cubit.dart';
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
  List<dynamic> smallTerminalMessages = [];

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

    // Display device info listener
    channel.on("displayDeviceInfo", (data) {
      // Update the list of terminal messages
      DeviceInfoDTO deviceInfoModel = DeviceInfoDTO.fromJson(data);

      setState(() {
        smallTerminalMessages.add(deviceInfoModel);
      });
    });

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

    return MultiBlocProvider(
      providers: [
        BlocProvider<OidCubit>(create: (_) => OidCubit()),
        BlocProvider<IpCubit>(create: (_) => IpCubit()),
        BlocProvider<CommunityCubit>(create: (_) => CommunityCubit()),
      ],
      child: GestureDetector(
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
                  const ThemeButton(),

                  const SizedBox(height: 20),

                  // IP address selection and OID selection
                  const Row(
                    children: [
                      Expanded(
                        child: Align(
                          alignment: Alignment.centerLeft,
                          child: IpSelection(),
                        ),
                      ),

                      Expanded(
                        child: Align(
                          alignment: Alignment.center,
                          child: OIdSelection(),
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
                  const Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Expanded(
                        child: Align(
                          alignment: Alignment.centerLeft,
                          child: CommunitySelection(),
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
                  const ScanningPortsElements(),

                  const SizedBox(height: 20),

                  // Allow/Forbid Port
                  const AllowForbitPortElements(),

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
      ),
    );
  }

  // Move the window to the center of the screen
  void moveWindowToCenter() async {
    await windowManager.center();
  }
}
