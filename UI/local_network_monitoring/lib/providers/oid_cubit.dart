import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class OidCubit extends Cubit<OidState> {
  OidCubit() : super(OidState(oidController: TextEditingController()));

  final TextEditingController oidController = TextEditingController();

  void onOidChanged(String value) {
    emit(state.copyWith(oid: value));
  }
}

class OidState {
  final TextEditingController oidController;
  final String oid;

  // OID that can be used - '1.3.6.1.2.1.1'
  OidState({required this.oidController, this.oid = ""});

  OidState copyWith({
    TextEditingController? oidController,
    String? oid,
  }) {
    return OidState(
      oidController: oidController ?? this.oidController,
      oid: oid ?? this.oid,
    );
  }
}
