import 'dart:async';

import 'package:dropdown_button2/dropdown_button2.dart';
import 'package:flutter/material.dart';
import 'package:local_network_monitoring/utils/constants.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HistoryTextField extends StatefulWidget {
  final String fieldType;
  final String hintText;
  final TextEditingController controller;

  const HistoryTextField({
    super.key,
    required this.fieldType,
    required this.hintText,
    required this.controller,
  });

  @override
  State<HistoryTextField> createState() => _HistoryTextFieldState();
}

class _HistoryTextFieldState extends State<HistoryTextField> {
  final List<String> _history = [];
  String? _selectedHistory;
  Timer? _debounce;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  @override
  void dispose() {
    widget.controller.dispose();
    _debounce?.cancel();
    super.dispose();
  }

  void _appendDefaultHistory() {
    switch (widget.fieldType) {
      case "ipHistory":
        _history.add(defaultIp);
      case "oidField":
        _history.add(defaultOID);
      case "communityField":
        _history.add(defaultCommunity);
      case "fromPortField":
        _history.add(defaultFromPort);
      case "toPortField":
        _history.add(defaultToPort);
      case "controlPortField":
        _history.add(defaultFromPort);
    }
  }

  Future<void> _loadHistory() async {
    final preferences = await SharedPreferences.getInstance();
    setState(() {
      _history.addAll(preferences.getStringList(widget.fieldType) ?? []);
      if (_history.isNotEmpty) {
        _selectedHistory = _history.first;
        widget.controller.text = _selectedHistory!;
      } else {
        _appendDefaultHistory();
        _saveHistory();
      }
    });
  }

  Future<void> _saveHistory() async {
    final preferences = await SharedPreferences.getInstance();
    preferences.setStringList(widget.fieldType, _history);
  }

  bool _isValidObject(String fieldType) {
    switch (fieldType) {
      case "ipHistory":
        return _isValidIP(widget.controller.text);
      case "oidField":
        return widget.controller.text.isNotEmpty;
      case "communityField":
        return widget.controller.text.isNotEmpty;
      default:
        return false;
    }
  }

  void _addToHistory(String text) {
    if (text.isNotEmpty && !_history.contains(text)) {
      if (_isValidObject(widget.fieldType)) {
        _history.insert(0, text);
        _saveHistory();
      }
    }
  }

  bool _isValidIP(String ip) {
    final ipv4Regex = RegExp(
        r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$');

    return ipv4Regex.hasMatch(ip);
  }

  void _onChanged(String value) {
    // Handles adding result to history with a little delay so user can finish input
    if (_debounce?.isActive ?? false) _debounce?.cancel();
    _debounce = Timer(
      const Duration(milliseconds: 500),
      () {
        _addToHistory(value);
        setState(
          () {
            _selectedHistory = null;
          },
        );
      },
    );
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
                hintStyle: const TextStyle(
                  fontSize: 10,
                ),
                hintText: widget.hintText,
              ),
              controller: widget.controller,
              onChanged: _onChanged,
            ),
          ),
          SizedBox(
            width: 30,
            child: DropdownButtonHideUnderline(
              child: DropdownButton2(
                isExpanded: true,
                value: _selectedHistory,
                onChanged: (String? newValue) {
                  setState(() {
                    _selectedHistory = newValue;
                    widget.controller.text = newValue!;
                  });
                },
                selectedItemBuilder: (BuildContext context) {
                  // Return empty containers or a placeholder for the button
                  return _history.map((String value) {
                    return const SizedBox.shrink(); // Keeps the button empty
                  }).toList();
                },
                items: _history.map((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(
                      value,
                      style: const TextStyle(fontSize: 12),
                    ),
                  );
                }).toList(),
                buttonStyleData: const ButtonStyleData(
                  width: 30,
                  height: 40,
                  padding: EdgeInsets.all(0), // Compact padding
                ),
                dropdownStyleData: const DropdownStyleData(
                  maxHeight: 200,
                  width: 150,
                  padding: EdgeInsets.symmetric(horizontal: 8),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.all(Radius.circular(5)),
                    color: Colors.white, // Dropdown background color
                  ),
                  elevation: 2, // Shadow
                ),
                menuItemStyleData: const MenuItemStyleData(
                  height: 40, // Height of each menu item
                  padding: EdgeInsets.symmetric(horizontal: 8),
                ),
                iconStyleData: const IconStyleData(
                  icon: Icon(Icons.arrow_drop_down),
                  iconSize: 16,
                  iconEnabledColor: Colors.black,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
