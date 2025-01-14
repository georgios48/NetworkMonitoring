import 'package:dio/dio.dart';
import 'package:local_network_monitoring/api/routes.dart';

class APIService {
  final APIRoutes _apiRoutes = APIRoutes();
  final dio = Dio();

  // Get info for ports scanned in given range
  Future<void> getInfoForPortsInRange(String fromRange, String toRange) async {
    // Convert body in a way that backend can read it
    final data = {"toPort": toRange, "fromPort": fromRange};

    try {
      final response = await dio.post(_apiRoutes.scanPortsRangeURL, data: data);
      print("Vs tochno: ${response}");
    } on DioException catch (e) {
      if (e.response != null) {
        print(
            "Failed to post: ${e.response?.statusCode} ${e.response?.statusMessage}");
      } else {
        print("Unexpected error: ${e.message}");
      }
    }
  }
}
