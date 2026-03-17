import 'package:flutter/material.dart';
import '../models/medication_model.dart';
import '../services/api_service.dart';

/// 用药管理状态管理
class MedicationProvider extends ChangeNotifier {
  List<MedicationModel> _medications = [];
  List<MedicationModel> _todayMedications = [];
  bool _isLoading = false;

  List<MedicationModel> get medications => _medications;
  List<MedicationModel> get todayMedications => _todayMedications;
  bool get isLoading => _isLoading;

  /// 加载用药列表
  Future<void> loadMedications() async {
    try {
      _isLoading = true;
      notifyListeners();

      final response = await ApiService.instance.get('/medications');
      if (response.statusCode == 200) {
        final List<dynamic> medicationsJson = response.data['data'];
        _medications = medicationsJson
            .map((json) => MedicationModel.fromJson(json))
            .toList();
        
        _filterTodayMedications();
      }
    } catch (e) {
      // 处理错误
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// 筛选今日用药
  void _filterTodayMedications() {
    final now = DateTime.now();
    _todayMedications = _medications.where((med) {
      return med.reminderTimes.any((time) {
        final reminderTime = DateTime.parse(time);
        return reminderTime.hour == now.hour && reminderTime.minute == now.minute;
      });
    }).toList();
  }

  /// 添加用药
  Future<bool> addMedication(MedicationModel medication) async {
    try {
      _isLoading = true;
      notifyListeners();

      final response = await ApiService.instance.post(
        '/medications',
        data: medication.toJson(),
      );

      if (response.statusCode == 200) {
        await loadMedications();
        return true;
      }
      return false;
    } catch (e) {
      return false;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// 更新用药
  Future<bool> updateMedication(MedicationModel medication) async {
    try {
      final response = await ApiService.instance.put(
        '/medications/${medication.id}',
        data: medication.toJson(),
      );

      if (response.statusCode == 200) {
        await loadMedications();
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  /// 删除用药
  Future<bool> deleteMedication(String medicationId) async {
    try {
      final response = await ApiService.instance.delete(
        '/medications/$medicationId',
      );

      if (response.statusCode == 200) {
        await loadMedications();
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  /// 标记为已服用
  Future<bool> markAsTaken(String medicationId) async {
    try {
      final response = await ApiService.instance.post(
        '/medications/$medicationId/take',
      );

      if (response.statusCode == 200) {
        await loadMedications();
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }
}
