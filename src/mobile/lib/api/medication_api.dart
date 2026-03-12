import '../services/api_service.dart';

/// 用药 API 服务
class MedicationApi {
  static const String _basePath = '/medications';

  /// 获取用药列表
  static Future<List<Map<String, dynamic>>> getMedications() async {
    try {
      final response = await ApiService.instance.get(_basePath);
      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(response.data['data']);
      }
      throw Exception('获取用药列表失败');
    } catch (e) {
      rethrow;
    }
  }

  /// 添加用药
  static Future<bool> addMedication(Map<String, dynamic> data) async {
    try {
      final response = await ApiService.instance.post(_basePath, data);
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  /// 更新用药
  static Future<bool> updateMedication(String id, Map<String, dynamic> data) async {
    try {
      final response = await ApiService.instance.put('$_basePath/$id', data);
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  /// 删除用药
  static Future<bool> deleteMedication(String id) async {
    try {
      final response = await ApiService.instance.delete('$_basePath/$id');
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  /// 标记为已服用
  static Future<bool> markAsTaken(String id) async {
    try {
      final response = await ApiService.instance.post('$_basePath/$id/take');
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
