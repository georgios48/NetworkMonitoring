class ProcessDTO {
  final String process;

  ProcessDTO({required this.process});

  factory ProcessDTO.fromJson(Map<String, dynamic> json) {
    return ProcessDTO(process: json["process"]);
  }

  Map<String, dynamic> toJson() => {"process": process};
}
