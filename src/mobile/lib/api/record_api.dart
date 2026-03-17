import 'dart:io';
import 'package:dio/dio.dart';
import '../services/api_service.dart';

/// 档案 API 服务
class RecordApi {
  static const String _basePath = '/records';

  /// 获取档案列表
  static Future<Map<String, dynamic>> getRecords({
    int page = 1,
    int pageSize = 20,
    String? recordType,
    int? memberId,
  }) async {
    try {
      final response = await ApiService.instance.get(
        _basePath,
        queryParameters: {
          'page': page,
          'page_size': pageSize,
          if (recordType != null) 'record_type': recordType,
          if (memberId != null) 'member_id': memberId,
        },
      );

      if (response.statusCode == 200) {
        return response.data['data'];
      }
      throw Exception('获取档案列表失败');
    } catch (e) {
      rethrow;
    }
  }

  /// 获取档案详情
  static Future<Map<String, dynamic>> getRecordDetail(String recordId) async {
    try {
      final response = await ApiService.instance.get('$_basePath/$recordId');
      if (response.statusCode == 200) {
        return response.data['data'];
      }
      throw Exception('获取档案详情失败');
    } catch (e) {
      rethrow;
    }
  }

  /// 上传档案
  static Future<Map<String, dynamic>> uploadRecord({
    required String filePath,
    required String recordType,
    required String title,
    required String recordDate,
    int? memberId,
    String? hospital,
    String? department,
  }) async {
    try {
      final file = File(filePath);
      final fileName = filePath.split('/').last;

      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          file.path,
          filename: fileName,
        ),
        'record_type': recordType,
        'title': title,
        'record_date': recordDate,
        if (memberId != null) 'member_id': memberId,
        if (hospital != null) 'hospital': hospital,
        if (department != null) 'department': department,
      });

      final response = await ApiService.instance.post(
        '$_basePath/upload',
        data: formData,
      );

      if (response.statusCode == 200) {
        return response.data['data'];
      }
      throw Exception('上传失败');
    } catch (e) {
      rethrow;
    }
  }

  /// 删除档案
  static Future<bool> deleteRecord(String recordId) async {
    try {
      final response = await ApiService.instance.delete('$_basePath/$recordId');
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
