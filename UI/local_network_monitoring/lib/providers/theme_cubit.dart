/*

THEME PROVIDER

Used to change APP theme between light and dark mode

*/

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:local_network_monitoring/themes/dark_mode.dart';
import 'package:local_network_monitoring/themes/light_mode.dart';

class ThemeCubit extends Cubit<ThemeData> {
  // Set initial theme -> lightMode
  bool _isDarkMode = false;
  ThemeCubit() : super(lightMode);

  bool get isDarkMode => _isDarkMode;

  void toggleTheme() {
    // Switch between light and dark mode

    _isDarkMode = !_isDarkMode;
    emit(_isDarkMode ? darkMode : lightMode);
  }
}
