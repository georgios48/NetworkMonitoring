import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class IpCubit extends Cubit<IpState> {
  IpCubit() : super(IpState(ipController: TextEditingController()));

  final TextEditingController ipController = TextEditingController();

  void onIpChanged(String value) {
    emit(state.copyWith(ip: value));
  }
}

class IpState {
  final TextEditingController ipController;
  final String ip;

  // Default IP that can be used - 194.141.37.238'
  IpState({required this.ipController, this.ip = ""});

  IpState copyWith({
    TextEditingController? ipController,
    String? ip,
  }) {
    return IpState(
      ipController: ipController ?? this.ipController,
      ip: ip ?? this.ip,
    );
  }
}
