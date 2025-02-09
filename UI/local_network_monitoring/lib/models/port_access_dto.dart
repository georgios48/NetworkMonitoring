class PortAccessDTO {
  final String message;

  PortAccessDTO({required this.message});

  // Factory constructor to create a DTO from the received data
  factory PortAccessDTO.fromString(String msg) {
    return PortAccessDTO(message: msg);
  }

  // Convert DTO back to JSON if needed
  Map<String, dynamic> toJson() {
    return {'message': message};
  }
}
