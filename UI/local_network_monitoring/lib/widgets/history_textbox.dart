import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HistoryTextField extends StatefulWidget {
  final String fieldType;
  final String hintText;
  final TextEditingController controller;

  const HistoryTextField(
      {super.key,
      required this.fieldType,
      required this.hintText,
      required this.controller});

  @override
  State<HistoryTextField> createState() => _HistoryTextFieldState();
}

class _HistoryTextFieldState extends State<HistoryTextField> {
  final List<String> _history = [];
  String? _selectedHistory;

  @override
  void initState() {
    super.initState();
    // Load history from storage
    _loadHistory();
  }

  @override
  void dispose() {
    widget.controller.dispose();
    super.dispose();
  }

  Future<void> _loadHistory() async {
    // Load history from storage
    final preferences = await SharedPreferences.getInstance();

    setState(() {
      _history.addAll(preferences.getStringList(widget.fieldType) ?? []);

      if (_history.isNotEmpty) {
        _selectedHistory = _history.first;
        widget.controller.text = _selectedHistory!;
      }
    });
  }

  Future<void> _saveHistory() async {
    // Save history to storage
    final preferences = await SharedPreferences.getInstance();
    preferences.setStringList(widget.fieldType, _history);
  }

  void _addToHistory(String text) {
    if (text.isNotEmpty && !_history.contains(text)) {
      _history.insert(0, text);
      // Save history to storage
      _saveHistory();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).scaffoldBackgroundColor,
        border: Border.all(color: Theme.of(context).dividerColor),
        borderRadius: BorderRadius.circular(5),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              cursorColor: Theme.of(context).dividerColor,
              decoration: InputDecoration(
                border: InputBorder.none,
                hintText: widget.hintText,
                hintStyle: const TextStyle(
                  overflow: TextOverflow.ellipsis,
                  fontSize: 9,
                  fontWeight: FontWeight.bold,
                ),
              ),
              controller: widget.controller,
              onChanged: (value) {
                setState(() {
                  _selectedHistory = null;
                });
              },
              onSubmitted: (value) {
                _addToHistory(value);
              },
            ),
          ),
          SizedBox(
            width: 50,
            child: DropdownButtonHideUnderline(
              child: DropdownButton<String>(
                isExpanded: true,
                value: _selectedHistory,
                onChanged: (String? newValue) {
                  setState(() {
                    _selectedHistory = newValue;
                    widget.controller.text = newValue!;
                  });
                },
                selectedItemBuilder: (BuildContext context) {
                  return _history.map<Widget>((String value) {
                    return Container();
                  }).toList();
                },
                items: _history.map<DropdownMenuItem<String>>((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(
                      value,
                      textAlign: TextAlign.left,
                    ),
                  );
                }).toList(),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
