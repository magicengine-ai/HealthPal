import 'package:equatable/equatable.dart';

/// 健康档案模型
class RecordModel extends Equatable {
  final String id;
  final String uuid;
  final int userId;
  final String recordType;
  final String title;
  final String recordDate;
  final String? hospital;
  final String? department;
  final List<String> files;
  final int ocrStatus; // 0-待处理 1-处理中 2-完成 3-失败
  final String? ocrMessage;
  final List<IndicatorModel> indicators;
  final List<String> tags;
  final DateTime createdAt;

  const RecordModel({
    required this.id,
    required this.uuid,
    required this.userId,
    required this.recordType,
    required this.title,
    required this.recordDate,
    this.hospital,
    this.department,
    this.files = const [],
    this.ocrStatus = 0,
    this.ocrMessage,
    this.indicators = const [],
    this.tags = const [],
    required this.createdAt,
  });

  factory RecordModel.fromJson(Map<String, dynamic> json) {
    return RecordModel(
      id: json['id']?.toString() ?? '',
      uuid: json['uuid'] ?? '',
      userId: json['user_id'] ?? 0,
      recordType: json['record_type'] ?? '',
      title: json['title'] ?? '',
      recordDate: json['record_date'] ?? '',
      hospital: json['hospital'],
      department: json['department'],
      files: json['files'] != null 
          ? List<String>.from(json['files']) 
          : [],
      ocrStatus: json['ocr_status'] ?? 0,
      ocrMessage: json['ocr_message'],
      indicators: json['indicators'] != null
          ? (json['indicators'] as List)
              .map((i) => IndicatorModel.fromJson(i))
              .toList()
          : [],
      tags: json['tags'] != null 
          ? List<String>.from(json['tags']) 
          : [],
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'uuid': uuid,
      'user_id': userId,
      'record_type': recordType,
      'title': title,
      'record_date': recordDate,
      'hospital': hospital,
      'department': department,
      'files': files,
      'ocr_status': ocrStatus,
      'ocr_message': ocrMessage,
      'indicators': indicators.map((i) => i.toJson()).toList(),
      'tags': tags,
      'created_at': createdAt.toIso8601String(),
    };
  }

  @override
  List<Object?> get props => [
        id,
        uuid,
        userId,
        recordType,
        title,
        recordDate,
        hospital,
        department,
        files,
        ocrStatus,
        ocrMessage,
        indicators,
        tags,
        createdAt,
      ];

  /// 获取 OCR 状态文本
  String get ocrStatusText {
    switch (ocrStatus) {
      case 0:
        return '待处理';
      case 1:
        return '识别中';
      case 2:
        return '已完成';
      case 3:
        return '识别失败';
      default:
        return '未知';
    }
  }

  /// 获取档案类型文本
  String get recordTypeText {
    switch (recordType) {
      case '体检':
        return '体检报告';
      case '病历':
        return '病历';
      case '检查':
        return '检查报告';
      case '化验':
        return '化验单';
      default:
        return recordType;
    }
  }
}

/// 健康指标模型
class IndicatorModel extends Equatable {
  final String id;
  final String name;
  final String code;
  final double value;
  final String unit;
  final String? referenceRange;
  final String status; // normal/warning/critical
  final String? category;

  const IndicatorModel({
    required this.id,
    required this.name,
    required this.code,
    required this.value,
    required this.unit,
    this.referenceRange,
    required this.status,
    this.category,
  });

  factory IndicatorModel.fromJson(Map<String, dynamic> json) {
    return IndicatorModel(
      id: json['id']?.toString() ?? '',
      name: json['name'] ?? '',
      code: json['code'] ?? '',
      value: (json['value'] ?? 0).toDouble(),
      unit: json['unit'] ?? '',
      referenceRange: json['reference_range'],
      status: json['status'] ?? 'normal',
      category: json['category'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'code': code,
      'value': value,
      'unit': unit,
      'reference_range': referenceRange,
      'status': status,
      'category': category,
    };
  }

  @override
  List<Object?> get props => [
        id,
        name,
        code,
        value,
        unit,
        referenceRange,
        status,
        category,
      ];

  /// 获取状态图标
  String get statusIcon {
    switch (status) {
      case 'normal':
        return '✅';
      case 'warning':
        return '⚠️';
      case 'critical':
        return '🚨';
      default:
        return '❓';
    }
  }

  /// 获取状态文本
  String get statusText {
    switch (status) {
      case 'normal':
        return '正常';
      case 'warning':
        return '异常';
      case 'critical':
        return '危急';
      default:
        return '未知';
    }
  }
}
