import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class CommunityCubit extends Cubit<CommunityState> {
  CommunityCubit()
      : super(CommunityState(communityController: TextEditingController()));

  final TextEditingController communityController = TextEditingController();

  void onCommunityChanged(String value) {
    emit(state.copyWith(community: value));
  }
}

class CommunityState {
  final TextEditingController communityController;
  final String community;

  // Default community that can be used - "public"
  CommunityState({required this.communityController, this.community = ""});

  CommunityState copyWith({
    TextEditingController? communityController,
    String? community,
  }) {
    return CommunityState(
      communityController: communityController ?? this.communityController,
      community: community ?? this.community,
    );
  }
}
