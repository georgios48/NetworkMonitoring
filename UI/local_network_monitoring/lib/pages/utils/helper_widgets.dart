// ----------------- Helper Widgets for UI Page -----------------

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:local_network_monitoring/api/api_service.dart';
import 'package:local_network_monitoring/themes/theme_cubit.dart';
import 'package:local_network_monitoring/widgets/button.dart';
import 'package:local_network_monitoring/widgets/history_textbox.dart';
import 'package:local_network_monitoring/widgets/output_terminal.dart';

// ---- Private ----
class ThemeButton extends StatelessWidget {
  // Change theme button widget
  const ThemeButton({super.key});

  @override
  Widget build(BuildContext context) {
    // Theme Cubit
    final themeCubit = context.watch<ThemeCubit>();
    // Check is DarkMode

    return IconButton(
      onPressed: () {
        themeCubit.toggleTheme();
      },
      icon: themeCubit.isDarkMode
          ? const Icon(Icons.dark_mode_outlined)
          : const Icon(Icons.light_mode_outlined),
    );
  }
}

class IpSelection extends StatelessWidget {
  final TextEditingController controller;

  const IpSelection({super.key, required this.controller});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Text("IP Адрес: ", style: TextStyle(fontWeight: FontWeight.bold)),

        const SizedBox(width: 20),

        // IP Address text field
        SizedBox(
            width: 200,
            child: HistoryTextField(
              fieldType: "ipField",
              hintText: "Въведете IP адрес",
              controller: controller,
            ))
      ],
    );
  }
}

class OIdSelection extends StatelessWidget {
  final TextEditingController controller;

  const OIdSelection({super.key, required this.controller});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Text("Обект ID: ", style: TextStyle(fontWeight: FontWeight.bold)),

        const SizedBox(width: 64),

        // OID Address text field
        SizedBox(
            width: 200,
            child: HistoryTextField(
              fieldType: "oidField",
              hintText: "Въведете OID",
              controller: controller,
              // borderColor: null,
            ))
      ],
    );
  }
}

class InfoForDeviceButton extends StatelessWidget {
  const InfoForDeviceButton({super.key});

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      buttonText: "Извеждане на информация за това устройство",
      customOnPressed: () {},
    );
  }
}

class CommunitySelection extends StatelessWidget {
  final TextEditingController controller;

  const CommunitySelection({super.key, required this.controller});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Text("Community: ",
            style: TextStyle(fontWeight: FontWeight.bold)),

        const SizedBox(height: 20),

        // Community text field
        SizedBox(
          width: 200,
          child: HistoryTextField(
            fieldType: "communityField",
            hintText: "Community",
            controller: controller,
            // borderColor: Colors.red,
          ),
        ),
      ],
    );
  }
}

class StopScanningButton extends StatelessWidget {
  const StopScanningButton({super.key});

  @override
  Widget build(BuildContext context) {
    ApiService service = ApiService();

    return CustomButton(
      buttonText: "Спри сканирането",
      customOnPressed: () {
        service.stopRunningProcess();
      },
      buttonColor: const Color(0xFFD22B2B),
    );
  }
}

// Widget that will be responsible for the output terminals
class TerminalWidget extends StatelessWidget {
  final List<dynamic> terminalMessages;
  final int flexSpaceToTake;
  const TerminalWidget(
      {super.key,
      required this.flexSpaceToTake,
      required this.terminalMessages});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: flexSpaceToTake,
      child: SizedBox(
        height: double.infinity,
        child: Terminal(messages: terminalMessages),
      ),
    );
  }
}

class AllowForbitPortElements extends StatefulWidget {
  const AllowForbitPortElements({super.key});

  @override
  State<AllowForbitPortElements> createState() =>
      _AllowForbitPortElementsState();
}

class _AllowForbitPortElementsState extends State<AllowForbitPortElements> {
  final TextEditingController portSelectionController = TextEditingController();

  @override
  void initState() {
    portSelectionController.addListener(() {
      setState(() {});
    });

    super.initState();
  }

  @override
  void dispose() {
    portSelectionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Expanded(
          child: Align(
            alignment: Alignment.centerLeft,
            child: _AllowPortButton(),
          ),
        ),
        Expanded(
          child: Align(
            alignment: Alignment.centerRight,
            child: _ControlPortField(controller: portSelectionController),
          ),
        ),
        const Expanded(
          child: Align(
            alignment: Alignment.centerRight,
            child: _ForbidPortButton(),
          ),
        ),
      ],
    );
  }
}

class ScanningPortsElements extends StatefulWidget {
  const ScanningPortsElements({super.key});

  @override
  State<ScanningPortsElements> createState() => _ScanningPortsElementsState();
}

class _ScanningPortsElementsState extends State<ScanningPortsElements> {
  final TextEditingController fromPortController = TextEditingController();
  final TextEditingController toPortController = TextEditingController();

  @override
  void initState() {
    fromPortController.addListener(() {
      setState(() {});
    });

    toPortController.addListener(() {
      setState(() {});
    });

    super.initState();
  }

  @override
  void dispose() {
    fromPortController.dispose();
    toPortController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
            child: Align(
          alignment: Alignment.centerLeft,
          child: _FromPortField(controller: fromPortController),
        )),

        Expanded(
          child: Align(
            alignment: Alignment.center,
            child: _ToPortField(controller: toPortController),
          ),
        ),

        // TODO: make button disabled if range isnt provided
        // Scan range of ports button and scan all ports button
        Expanded(
          child: Align(
            alignment: Alignment.centerRight,
            child:
                _ScanRangePorts(fromPortController.text, toPortController.text),
          ),
        ),

        // Scan all ports button
        const Expanded(
          child: Align(
            alignment: Alignment.centerRight,
            child: _ScanAllPortsButton(),
          ),
        ),
      ],
    );
  }
}

// End of helper widgets

// ---- Private widgets ---- //

class _FromPortField extends StatelessWidget {
  final TextEditingController controller;

  const _FromPortField({required this.controller});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Text("От порт: ", style: TextStyle(fontWeight: FontWeight.bold)),

        const SizedBox(width: 20),

        // From port text field
        SizedBox(
            width: 200,
            child: HistoryTextField(
              fieldType: "fromPortField",
              hintText: "Въведете начален порт",
              controller: controller,
            ))
      ],
    );
  }
}

class _ToPortField extends StatelessWidget {
  final TextEditingController controller;

  const _ToPortField({required this.controller});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Text("До порт: ", style: TextStyle(fontWeight: FontWeight.bold)),

        const SizedBox(width: 20),

        // To port text field
        SizedBox(
            width: 200,
            child: HistoryTextField(
              fieldType: "toPortField",
              hintText: "Въведете последен порт",
              controller: controller,
            ))
      ],
    );
  }
}

class _ScanRangePorts extends StatelessWidget {
  final String fromPort;
  final String toPort;
  const _ScanRangePorts(this.fromPort, this.toPort);

  @override
  Widget build(BuildContext context) {
    ApiService service = ApiService();
    return CustomButton(
      buttonText: "Сканиране на диапазон от портове",
      customOnPressed: () {
        service.getInfoForPortsInRange(fromPort, toPort);
      },
    );
  }
}

class _ScanAllPortsButton extends StatelessWidget {
  const _ScanAllPortsButton();

  @override
  Widget build(BuildContext context) {
    ApiService service = ApiService();
    return CustomButton(
      buttonText: "Сканиране на всички портове",
      customOnPressed: () {
        service.getInfoForPortsInRange("1", "24");
      },
    );
  }
}

class _AllowPortButton extends StatelessWidget {
  const _AllowPortButton();

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      buttonText: "Разрешаване на порт",
      customOnPressed: () {},
      buttonColor: Colors.green,
    );
  }
}

class _ControlPortField extends StatelessWidget {
  final TextEditingController controller;

  const _ControlPortField({required this.controller});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Text("Номер на порт: ",
            style: TextStyle(fontWeight: FontWeight.bold)),

        const SizedBox(width: 20),

        // To port text field
        SizedBox(
            width: 200,
            child: HistoryTextField(
              fieldType: "controlPortField",
              hintText: "Въведете номер на порт",
              controller: controller,
            ))
      ],
    );
  }
}

class _ForbidPortButton extends StatelessWidget {
  const _ForbidPortButton();

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      buttonText: "Забраняване на порт",
      customOnPressed: () {},
      buttonColor: const Color(0xFFD22B2B),
    );
  }
}
