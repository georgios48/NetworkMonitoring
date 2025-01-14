import 'package:flutter/material.dart';

class Terminal extends StatelessWidget {
  const Terminal({super.key});

  @override
  Widget build(BuildContext context) {
    List<String> test = List.generate(
      100, // Generate 100 lines of output
      (index) =>
          "Line ${index + 1}: This is a long line of text to test scrolling. "
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
          "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    );
    return SingleChildScrollView(
      child: Container(
        padding: const EdgeInsets.all(12),
        color: Colors.grey,
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: test.map((output) {
              // Make text selectable in the terminal in order to be able to cpy paste
              return SelectionArea(
                child: Text(
                  output,
                  style: const TextStyle(color: Colors.white),
                ),
              );
            }).toList(), // Here's the fix: toList() converts the iterable to a List<Widget>
          ),
        ),
      ),
    );
  }
}
