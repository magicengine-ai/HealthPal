import 'package:hive_flutter/hive_flutter.dart';

/// 本地存储服务
class StorageService {
  static const String _userBoxName = 'user_box';
  static const String _settingsBoxName = 'settings_box';
  static const String _cacheBoxName = 'cache_box';

  static late Box _userBox;
  static late Box _settingsBox;
  static late Box _cacheBox;

  /// 初始化存储
  static Future<void> init() async {
    _userBox = await Hive.openBox(_userBoxName);
    _settingsBox = await Hive.openBox(_settingsBoxName);
    _cacheBox = await Hive.openBox(_cacheBoxName);
  }

  // ========== User Box ==========

  /// 保存用户 ID
  static Future<void> saveUserId(String userId) async {
    await _userBox.put('user_id', userId);
  }

  /// 获取用户 ID
  static String? getUserId() {
    return _userBox.get('user_id');
  }

  /// 保存用户信息
  static Future<void> saveUserInfo(Map<String, dynamic> userInfo) async {
    await _userBox.put('user_info', userInfo);
  }

  /// 获取用户信息
  static Map<String, dynamic>? getUserInfo() {
    return _userBox.get('user_info');
  }

  /// 清除用户数据
  static Future<void> clearUserData() async {
    await _userBox.clear();
  }

  // ========== Settings Box ==========

  /// 保存设置
  static Future<void> saveSetting(String key, dynamic value) async {
    await _settingsBox.put(key, value);
  }

  /// 获取设置
  static T? getSetting<T>(String key, {T? defaultValue}) {
    return _settingsBox.get(key, defaultValue: defaultValue);
  }

  /// 清除所有设置
  static Future<void> clearSettings() async {
    await _settingsBox.clear();
  }

  // ========== Cache Box ==========

  /// 保存缓存
  static Future<void> saveCache(String key, dynamic value) async {
    await _cacheBox.put(key, value);
  }

  /// 获取缓存
  static T? getCache<T>(String key, {T? defaultValue}) {
    return _cacheBox.get(key, defaultValue: defaultValue);
  }

  /// 清除缓存
  static Future<void> clearCache() async {
    await _cacheBox.clear();
  }

  /// 清除所有数据
  static Future<void> clearAll() async {
    await _userBox.clear();
    await _settingsBox.clear();
    await _cacheBox.clear();
  }
}
