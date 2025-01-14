import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  final String buttonText;
  final VoidCallback customOnPressed;
  final Color? buttonColor;

  const CustomButton(
      {super.key,
      required this.buttonText,
      required this.customOnPressed,
      this.buttonColor});

  @override
  Widget build(BuildContext context) {
    return TextButton(
      onPressed: customOnPressed,
      style: ButtonStyle(
        shape: WidgetStateProperty.all<RoundedRectangleBorder>(
          RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(5),
            side: BorderSide(color: Color(Colors.transparent.value)),
          ),
        ),

        // Button color
        backgroundColor: WidgetStateProperty.all(
            buttonColor ?? Theme.of(context).colorScheme.primary),

        // Change color animation
        overlayColor:
            WidgetStateProperty.resolveWith<Color?>((Set<WidgetState> states) {
          if (states.contains(WidgetState.hovered)) {
            return Colors.grey.withOpacity(0.3);
          }
          if (states.contains(WidgetState.focused)) {
            return Colors.grey.withOpacity(0.3);
          }
          if (states.contains(WidgetState.pressed)) {
            return Colors.grey.withOpacity(0.3);
          }
          return Colors.transparent;
        }),
      ),
      child: Text(
        buttonText,
        style: TextStyle(
            color: buttonColor != null
                ? const Color(0xFFd8d8d8)
                : Theme.of(context).scaffoldBackgroundColor),
      ),
    );
  }
}
