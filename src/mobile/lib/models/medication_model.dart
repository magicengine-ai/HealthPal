import 'package:equatable/equatable.dart';

/// 用药模型
class MedicationModel extends Equatable {
  final String id;
  final String name;
  final String dosage;
  final String frequency;
  final List<String> reminderTimes;
  final String? startDate;
  final String? endDate;
  final int status; // 1-进行中 2-已完成 3-已停用
  final String? notes;
  final DateTime createdAt;

  const MedicationModel({
    required this.id,
    required this.name,
    required this.dosage,
    required this.frequency,
    required this.reminderTimes,
    this.startDate,
    this.endDate,
    this.status = 1,
    this.notes,
    required this.createdAt,
  });

  factory MedicationModel.fromJson(Map<String, dynamic> json) {
    return MedicationModel(
      id: json['id']?.toString() ?? '',
      name: json['name'] ?? '',
      dosage: json['dosage'] ?? '',
      frequency: json['frequency'] ?? '',
      reminderTimes: json['reminder_times'] != null
          ? List<String>.from(json['reminder_times'])
          : [],
      startDate: json['start_date'],
      endDate: json['end_date'],
      status: json['status'] ?? 1,
      notes: json['notes'],
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'dosage': dosage,
      'frequency': frequency,
      'reminder_times': reminderTimes,
      'start_date': startDate,
      'end_date': endDate,
      'status': status,
      'notes': notes,
      'created_at': createdAt.toIso8601String(),
    };
  }

  @override
  List<Object?> get props => [
        id,
        name,
        dosage,
        frequency,
        reminderTimes,
        startDate,
        endDate,
        status,
        notes,
        createdAt,
      ];

  /// 获取状态文本
  String get statusText {
    switch (status) {
      case 1:
        return '进行中';
      case 2:
        return '已完成';
      case 3:
        return '已停用';
      default:
        return '未知';
    }
  }

  /// 获取下次用药时间
  String? getNextDoseTime() {
    if (reminderTimes.isEmpty) return null;
    
    final now = DateTime.now();
    for (var time in reminderTimes) {
      final parts = time.split(':');
      final hour = int.parse(parts[0]);
      final minute = int.parse(parts[1]);
      final doseTime = DateTime(now.year, now.month, now.day, hour, minute);
      
      if (doseTime.isAfter(now)) {
        return time;
      }
    }
    
    // 如果今天的都已服用，返回明天的第一次
    return reminderTimes.first;
  }
}
