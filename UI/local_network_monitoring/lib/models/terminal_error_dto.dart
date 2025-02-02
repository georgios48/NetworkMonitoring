import 'dart:convert';

class TerminalError {
  final String? smallTerminalError;
  final String? bigTerminalError;

  TerminalError({this.smallTerminalError, this.bigTerminalError});

  factory TerminalError.fromJson(Map<String, dynamic> json) {
    String? smallError;
    String? bigError;

    // Check for both keys and assign the first one found.  Prioritizes smallTerminalError
    if (json.containsKey('smallTerminalError')) {
      smallError = json['smallTerminalError'] as String?;
    } else if (json.containsKey('bigTerminalError')) {
      bigError = json['bigTerminalError'] as String?;
    }

    return TerminalError(
      smallTerminalError: smallError,
      bigTerminalError: bigError,
    );
  }

  Map<String, dynamic> toJson() => {
        if (smallTerminalError != null)
          'smallTerminalError': smallTerminalError,
        if (bigTerminalError != null) 'bigTerminalError': bigTerminalError,
      };

  @override
  String toString() {
    return 'TerminalError{smallTerminalError: $smallTerminalError, bigTerminalError: $bigTerminalError}';
  }

  //Helper function for easy fromJson conversion
  static TerminalError? fromJsonString(String jsonString) {
    try {
      Map<String, dynamic> jsonMap = jsonDecode(jsonString);
      return TerminalError.fromJson(jsonMap);
    } catch (e) {
      print("Error decoding JSON: $e");
      return null;
    }
  }

  static String? extractMessage(String jsonString) {
    TerminalError? error = TerminalError.fromJsonString(jsonString);
    return error?.smallTerminalError ?? error?.bigTerminalError;
  }
}
