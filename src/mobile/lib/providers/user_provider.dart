import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/storage_service.dart';
import '../models/user_model.dart';

/// 用户状态管理
class UserProvider extends ChangeNotifier {
  UserModel? _currentUser;
  bool _isLoading = false;
  bool _isLoggedIn = false;

  UserModel? get currentUser => _currentUser;
  bool get isLoading => _isLoading;
  bool get isLoggedIn => _isLoggedIn;

  /// 初始化用户状态
  Future<void> init() async {
    final isLoggedIn = await ApiService.isLoggedIn();
    if (isLoggedIn) {
      await loadUserInfo();
    }
  }

  /// 加载用户信息
  Future<void> loadUserInfo() async {
    try {
      _isLoading = true;
      notifyListeners();

      // TODO: 从 API 获取用户信息
      // final response = await ApiService.instance.get('/users/me');
      // _currentUser = UserModel.fromJson(response.data);
      
      _isLoggedIn = true;
    } catch (e) {
      _isLoggedIn = false;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// 登录
  Future<bool> login(String phone, String password) async {
    try {
      _isLoading = true;
      notifyListeners();

      final response = await ApiService.instance.post(
        '/auth/login',
        {
          'phone': phone,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        await ApiService.saveToken(data['access_token']);
        _currentUser = UserModel.fromJson(data['user']);
        _isLoggedIn = true;
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

  /// 注册
  Future<bool> register(String phone, String password, String code) async {
    try {
      _isLoading = true;
      notifyListeners();

      final response = await ApiService.instance.post(
        '/auth/register',
        {
          'phone': phone,
          'password': password,
          'code': code,
        },
      );

      if (response.statusCode == 200) {
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

  /// 登出
  Future<void> logout() async {
    await ApiService.clearToken();
    await StorageService.clearUserData();
    _currentUser = null;
    _isLoggedIn = false;
    notifyListeners();
  }
}
