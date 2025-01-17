import 'package:flutter/material.dart';
import 'package:local_network_monitoring/models/port_scan.dart';

class Terminal extends StatefulWidget {
  final List<dynamic> messages;
  const Terminal({super.key, required this.messages});

  @override
  State<Terminal> createState() => _TerminalState();
}

class _TerminalState extends State<Terminal> {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Container(
        padding: const EdgeInsets.all(12),
        color: Colors.grey,
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: widget.messages.map(
              (output) {
                // Make text selectable in the terminal in order to be able to cpy paste
                if (output is PortScanModel) {
                  return SelectionArea(
                    child: Text(
                      // TODO: think of a way to scroll to botton and maybe clear previous terminal on a new call
                      "PortNumber ${output.number}, ${output.port}, status: ${output.ifAlias}, vlan: ${output.vlan}, In: ${output.inSpeed}, Out: ${output.outSpeed}, InError: ${output.inError}, OutError: ${output.outError}\n",
                      style: const TextStyle(color: Colors.white),
                    ),
                  );
                } else {
                  return SelectionArea(child: Text("test"));
                }
              },
            ).toList(), // Here's the fix: toList() converts the iterable to a List<Widget>
          ),
        ),
      ),
    );
  }
}
