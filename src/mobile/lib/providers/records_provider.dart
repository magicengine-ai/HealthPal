import 'package:flutter/material.dart';
import '../models/record_model.dart';
import '../services/api_service.dart';

/// 健康档案状态管理
class RecordsProvider extends ChangeNotifier {
  List<RecordModel> _records = [];
  bool _isLoading = false;
  int _page = 1;
  int _total = 0;
  bool _hasMore = true;

  List<RecordModel> get records => _records;
  bool get isLoading => _isLoading;
  int get page => _page;
  int get total => _total;
  bool get hasMore => _hasMore;

  /// 获取档案列表
  Future<void> loadRecords({
    int page = 1,
    int pageSize = 20,
    String? recordType,
    int? memberId,
    bool refresh = false,
  }) async {
    if (refresh) {
      _records.clear();
      _page = 1;
    }

    try {
      _isLoading = true;
      notifyListeners();

      final response = await ApiService.instance.get(
        '/records',
        queryParameters: {
          'page': page,
          'page_size': pageSize,
          if (recordType != null) 'record_type': recordType,
          if (memberId != null) 'member_id': memberId,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data['data'];
        final List<dynamic> recordsJson = data['records'];
        final newRecords = recordsJson
            .map((json) => RecordModel.fromJson(json))
            .toList();

        if (refresh) {
          _records = newRecords;
        } else {
          _records.addAll(newRecords);
        }

        _page = data['page'] + 1;
        _total = data['total'];
        _hasMore = _records.length < _total;
      }
    } catch (e) {
      // 处理错误
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// 获取档案详情
  Future<RecordModel?> getRecordDetail(String recordId) async {
    try {
      final response = await ApiService.instance.get('/records/$recordId');
      if (response.statusCode == 200) {
        return RecordModel.fromJson(response.data['data']);
      }
    } catch (e) {
      // 处理错误
    }
    return null;
  }

  /// 上传档案
  Future<bool> uploadRecord({
    required String filePath,
    required String recordType,
    required String title,
    required String recordDate,
    int? memberId,
    String? hospital,
    String? department,
  }) async {
    try {
      _isLoading = true;
      notifyListeners();

      // TODO: 实现文件上传
      // final formData = FormData.fromMap({...});
      // final response = await ApiService.instance.post('/records/upload', formData);

      return true;
    } catch (e) {
      return false;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// 删除档案
  Future<bool> deleteRecord(String recordId) async {
    try {
      final response = await ApiService.instance.delete('/records/$recordId');
      if (response.statusCode == 200) {
        _records.removeWhere((record) => record.id == recordId);
        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  /// 刷新档案列表
  Future<void> refresh() async {
    await loadRecords(refresh: true);
  }

  /// 加载更多
  Future<void> loadMore() async {
    if (!_isLoading && _hasMore) {
      await loadRecords(page: _page);
    }
  }
}
