// ----------------- Helper Widgets for UI Page -----------------

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:local_network_monitoring/themes/theme_cubit.dart';
import 'package:local_network_monitoring/widgets/button.dart';
import 'package:local_network_monitoring/widgets/history_textbox.dart';
import 'package:local_network_monitoring/widgets/output_terminal.dart';

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
  const IpSelection({super.key});

  @override
  Widget build(BuildContext context) {
    return const Row(
      children: [
        Text("IP Адрес: ", style: TextStyle(fontWeight: FontWeight.bold)),

        SizedBox(width: 20),

        // IP Address text field
        SizedBox(
            width: 200,
            child: HistoryTextField(
              fieldType: "ipField",
              hintText: "Въведете IP адрес",
              // borderColor: null,
            ))
      ],
    );
  }
}

class OIdSelection extends StatelessWidget {
  const OIdSelection({super.key});

  @override
  Widget build(BuildContext context) {
    return const Row(
      children: [
        Text("Обект ID: ", style: TextStyle(fontWeight: FontWeight.bold)),

        SizedBox(width: 64),

        // OID Address text field
        SizedBox(
            width: 200,
            child: HistoryTextField(
              fieldType: "oidField",
              hintText: "Въведете OID",
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
  const CommunitySelection({super.key});

  @override
  Widget build(BuildContext context) {
    return const Row(
      children: [
        Text("Community: ", style: TextStyle(fontWeight: FontWeight.bold)),

        SizedBox(height: 20),

        // Community text field
        SizedBox(
          width: 200,
          child: HistoryTextField(
            fieldType: "communityField",
            hintText: "Community",
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
    return CustomButton(
      buttonText: "Спри сканирането",
      customOnPressed: () {},
      buttonColor: const Color(0xFFD22B2B),
    );
  }
}

class FromPortField extends StatelessWidget {
  const FromPortField({super.key});

  @override
  Widget build(BuildContext context) {
    return const Row(
      children: [
        Text("От порт: ", style: TextStyle(fontWeight: FontWeight.bold)),

        SizedBox(width: 20),

        // From port text field
        SizedBox(
            width: 200,
            child: HistoryTextField(
              fieldType: "fromPortField",
              hintText: "Въведете начален порт",
            ))
      ],
    );
  }
}

class ToPortField extends StatelessWidget {
  const ToPortField({super.key});

  @override
  Widget build(BuildContext context) {
    return const Row(
      children: [
        Text("До порт: ", style: TextStyle(fontWeight: FontWeight.bold)),

        SizedBox(width: 20),

        // To port text field
        SizedBox(
            width: 200,
            child: HistoryTextField(
              fieldType: "toPortField",
              hintText: "Въведете последен порт",
            ))
      ],
    );
  }
}

class ScanRangePorts extends StatelessWidget {
  const ScanRangePorts({super.key});

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      buttonText: "Сканиране на диапазон от портове",
      customOnPressed: () {},
    );
  }
}

class ScanAllPortsButton extends StatelessWidget {
  const ScanAllPortsButton({super.key});

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      buttonText: "Сканиране на всички портове",
      customOnPressed: () {},
    );
  }
}

class AllowPortButton extends StatelessWidget {
  const AllowPortButton({super.key});

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      buttonText: "Разрешаване на порт",
      customOnPressed: () {},
      buttonColor: Colors.green,
    );
  }
}

class ControlPortField extends StatelessWidget {
  const ControlPortField({super.key});

  @override
  Widget build(BuildContext context) {
    return const Row(
      children: [
        Text("Номер на порт: ", style: TextStyle(fontWeight: FontWeight.bold)),

        SizedBox(width: 20),

        // To port text field
        SizedBox(
            width: 200,
            child: HistoryTextField(
              fieldType: "controlPortField",
              hintText: "Въведете номер на порт",
            ))
      ],
    );
  }
}

class ForbidPortButton extends StatelessWidget {
  const ForbidPortButton({super.key});

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      buttonText: "Забраняване на порт",
      customOnPressed: () {},
      buttonColor: const Color(0xFFD22B2B),
    );
  }
}

// Widget that will be responsible for the output terminals
class TerminalWidget extends StatelessWidget {
  final int flexSpaceToTake;
  const TerminalWidget({super.key, required this.flexSpaceToTake});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: flexSpaceToTake,
      child: const SizedBox(
        height: double.infinity,
        child: Terminal(),
      ),
    );
  }
}

// End of helper widgets
