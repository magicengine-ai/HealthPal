import 'package:equatable/equatable.dart';

/// 用户模型
class UserModel extends Equatable {
  final String id;
  final String phone;
  final String? nickname;
  final String? avatar;
  final int? gender;
  final String? birthday;
  final DateTime? createdAt;

  const UserModel({
    required this.id,
    required this.phone,
    this.nickname,
    this.avatar,
    this.gender,
    this.birthday,
    this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id']?.toString() ?? '',
      phone: json['phone'] ?? '',
      nickname: json['nickname'],
      avatar: json['avatar'],
      gender: json['gender'],
      birthday: json['birthday'],
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'phone': phone,
      'nickname': nickname,
      'avatar': avatar,
      'gender': gender,
      'birthday': birthday,
      'created_at': createdAt?.toIso8601String(),
    };
  }

  @override
  List<Object?> get props => [id, phone, nickname, avatar, gender, birthday, createdAt];
}
