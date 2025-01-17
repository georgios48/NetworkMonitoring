class PortScanModel {
  final int number;
  final String port;
  final String ifAlias;
  final String vlan;
  final String inSpeed;
  final String outSpeed;
  final int inError;
  final int outError;

  PortScanModel({
    required this.number,
    required this.port,
    required this.ifAlias,
    required this.vlan,
    required this.inSpeed,
    required this.outSpeed,
    required this.inError,
    required this.outError,
  });

  factory PortScanModel.fromJson(Map<String, dynamic> json) {
    return PortScanModel(
      number: json['number'],
      port: json['port'],
      ifAlias: json['ifAlias'],
      vlan: json['vlan'],
      inSpeed: json['In'].toString(), // Convert In to String
      outSpeed: json['Out'].toString(), // Convert Out to String
      inError: json['inError'],
      outError: json['outError'],
    );
  }

  Map<String, dynamic> toJson() => {
        'number': number,
        'port': port,
        'ifAlias': ifAlias,
        'vlan': vlan,
        'In': inSpeed,
        'Out': outSpeed,
        'inError': inError,
        'outError': outError,
      };
}
