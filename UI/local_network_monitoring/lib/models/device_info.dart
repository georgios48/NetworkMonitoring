class DeviceInfoDTO {
  final String systemOID;
  final String systemDevice;
  final String deviceModel;

  DeviceInfoDTO({
    required this.systemOID,
    required this.systemDevice,
    required this.deviceModel,
  });

  factory DeviceInfoDTO.fromJson(Map<String, dynamic> json) {
    return DeviceInfoDTO(
      systemOID: json['systemOID'] as String,
      systemDevice: json['systemDevice'] as String,
      deviceModel: json['deviceModel'] as String,
    );
  }

  Map<String, dynamic> toJson() => {
        'systemOID': systemOID,
        'systemDevice': systemDevice,
        'deviceModel': deviceModel,
      };
}
