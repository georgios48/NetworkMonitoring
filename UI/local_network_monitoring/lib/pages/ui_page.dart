import 'package:flutter/material.dart';
// ignore: unused_import
import "package:local_network_monitoring/pages/ui/utils/helper_widgets.dart";
import 'package:window_manager/window_manager.dart';

class UiPage extends StatefulWidget {
  const UiPage({super.key});

  @override
  State<UiPage> createState() => _UiPageState();
}

class _UiPageState extends State<UiPage> {
  @override
  Widget build(BuildContext context) {
    //! By double clicking, return the window into original position
    return GestureDetector(
      onDoubleTap: () {
        moveWindowToCenter();
      },
      child: const SafeArea(
        child: Scaffold(
          body: Padding(
            padding: EdgeInsets.fromLTRB(30, 30, 30, 5),
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
                      child: IpSelection(),
                    )),

                    Expanded(
                        child: Align(
                            alignment: Alignment.center,
                            child: OIdSelection())),

                    // Scan all devices button
                    Expanded(
                        child: Align(
                            alignment: Alignment.centerRight,
                            child: InfoForDeviceButton())),
                  ],
                ),

                SizedBox(height: 20),

                // Community and Stop Scan button
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Expanded(
                        child: Align(
                            alignment: Alignment.centerLeft,
                            child: CommunitySelection())),

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

                SizedBox(height: 20),

                // Scan range of ports
                Row(
                  children: [
                    Expanded(
                        child: Align(
                      alignment: Alignment.centerLeft,
                      child: FromPortField(),
                    )),

                    Expanded(
                      child: Align(
                          alignment: Alignment.center, child: ToPortField()),
                    ),

                    // Scan range of ports button and scan all ports button
                    Expanded(
                      child: Align(
                        alignment: Alignment.centerRight,
                        child: ScanRangePorts(),
                      ),
                    ),

                    // Scan all ports button
                    Expanded(
                      child: Align(
                        alignment: Alignment.centerRight,
                        child: ScanAllPortsButton(),
                      ),
                    ),
                  ],
                ),

                SizedBox(height: 20),

                // Allow/Forbid Port
                Row(
                  children: [
                    Expanded(
                      child: Align(
                        alignment: Alignment.centerLeft,
                        child: AllowPortButton(),
                      ),
                    ),
                    Expanded(
                      child: Align(
                        alignment: Alignment.centerRight,
                        child: ControlPortField(),
                      ),
                    ),
                    Expanded(
                      child: Align(
                        alignment: Alignment.centerRight,
                        child: ForbidPortButton(),
                      ),
                    ),
                  ],
                ),

                SizedBox(height: 10),

                // Terminal
                Expanded(
                  flex: 1,
                  child: Row(
                    children: [
                      TerminalWidget(
                        flexSpaceToTake: 2,
                      ),
                      SizedBox(width: 5),
                      Expanded(
                          child: TerminalWidget(
                        flexSpaceToTake: 1,
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
