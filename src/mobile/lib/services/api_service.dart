import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../utils/logger.dart';

/// API 服务配置
class ApiService {
  static late Dio _dio;
  static const String _baseUrl = 'http://localhost:8000/api/v1';
  static const String _tokenKey = 'access_token';

  static final FlutterSecureStorage _storage = const FlutterSecureStorage();

  static Future<void> init() async {
    _dio = Dio(
      BaseOptions(
        baseUrl: _baseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    // 添加拦截器
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // 添加认证 Token
          final token = await _storage.read(key: _tokenKey);
          if (token != null && token.isNotEmpty) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          AppLogger.d('Request: ${options.method} ${options.path}');
          return handler.next(options);
        },
        onResponse: (response, handler) {
          AppLogger.d('Response: ${response.statusCode} ${response.requestOptions.path}');
          return handler.next(response);
        },
        onError: (error, handler) {
          AppLogger.e('Error: ${error.response?.statusCode} ${error.requestOptions.path}');
          return handler.next(error);
        },
      ),
    );
  }

  static Dio get instance => _dio;

  /// 保存 Token
  static Future<void> saveToken(String token) async {
    await _storage.write(key: _tokenKey, value: token);
  }

  /// 获取 Token
  static Future<String?> getToken() async {
    return await _storage.read(key: _tokenKey);
  }

  /// 清除 Token
  static Future<void> clearToken() async {
    await _storage.delete(key: _tokenKey);
  }

  /// 检查是否已登录
  static Future<bool> isLoggedIn() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }
}
