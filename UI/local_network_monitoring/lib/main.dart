import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:local_network_monitoring/api/api_service.dart';
import 'package:local_network_monitoring/pages/ui_page.dart';
import 'package:local_network_monitoring/providers/theme_cubit.dart';
import 'package:screen_retriever/screen_retriever.dart';
import 'package:window_manager/window_manager.dart';

void main() async {
  // Set the windows to be maximum size and show the window
  WidgetsFlutterBinding.ensureInitialized();
  await WindowManager.instance.ensureInitialized();
  windowManager.waitUntilReadyToShow().then((_) async {
    await windowManager.setTitle("Local Network Monitoring");
    Display primaryDisplay = await screenRetriever.getPrimaryDisplay();
    double displayWidth = primaryDisplay.size.width;
    double displayHeight = primaryDisplay.size.height - 100;
    windowManager.setSize(Size(displayWidth, displayHeight));
    windowManager.center();
    windowManager.show();
    windowManager.focus();
    windowManager.setResizable(false);

    // Initialize WebSocket
    final apiService = SocketService();
    apiService.initializeWebSocket();
  });

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => ThemeCubit(),
      child: BlocBuilder<ThemeCubit, ThemeData>(
        builder: (context, theme) {
          return MaterialApp(
            title: 'Local Network Monitoring',
            theme: theme,
            home: const UiPage(),
            debugShowCheckedModeBanner: false,
          );
        },
      ),
    );
  }
}
