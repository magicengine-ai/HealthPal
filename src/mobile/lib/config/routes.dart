import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../screens/splash/splash_screen.dart';
import '../screens/auth/login_screen.dart';
import '../screens/auth/register_screen.dart';
import '../screens/home/home_screen.dart';
import '../screens/records/records_screen.dart';
import '../screens/records/record_detail_screen.dart';
import '../screens/records/upload_record_screen.dart';
import '../screens/analysis/analysis_screen.dart';
import '../screens/management/medication_screen.dart';
import '../screens/profile/profile_screen.dart';

/// 路由配置
class AppRouter {
  static const String splash = '/';
  static const String login = '/login';
  static const String register = '/register';
  static const String home = '/home';
  static const String records = '/records';
  static const String recordDetail = '/record/:id';
  static const String uploadRecord = '/records/upload';
  static const String analysis = '/analysis';
  static const String medication = '/medication';
  static const String profile = '/profile';

  static final GoRouter router = GoRouter(
    initialLocation: splash,
    routes: [
      // 启动页
      GoRoute(
        path: splash,
        name: 'splash',
        builder: (context, state) => const SplashScreen(),
      ),

      // 认证
      GoRoute(
        path: login,
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: register,
        name: 'register',
        builder: (context, state) => const RegisterScreen(),
      ),

      // 主页面（使用 ShellRoute 实现底部导航）
      ShellRoute(
        builder: (context, state, child) => HomeScreen(child: child),
        routes: [
          GoRoute(
            path: home,
            name: 'home',
            pageBuilder: (context, state) => NoTransitionPage(
              child: HomeScreen(child: const SizedBox.shrink()),
            ),
            routes: [
              GoRoute(
                path: records,
                name: 'records',
                parentNavigatorKey: _rootNavigatorKey,
                builder: (context, state) => const RecordsScreen(),
                routes: [
                  GoRoute(
                    path: ':id',
                    name: 'recordDetail',
                    parentNavigatorKey: _rootNavigatorKey,
                    builder: (context, state) => RecordDetailScreen(
                      recordId: state.pathParameters['id']!,
                    ),
                  ),
                  GoRoute(
                    path: 'upload',
                    name: 'uploadRecord',
                    parentNavigatorKey: _rootNavigatorKey,
                    builder: (context, state) => const UploadRecordScreen(),
                  ),
                ],
              ),
              GoRoute(
                path: analysis,
                name: 'analysis',
                parentNavigatorKey: _rootNavigatorKey,
                builder: (context, state) => const AnalysisScreen(),
              ),
              GoRoute(
                path: medication,
                name: 'medication',
                parentNavigatorKey: _rootNavigatorKey,
                builder: (context, state) => const MedicationScreen(),
              ),
              GoRoute(
                path: profile,
                name: 'profile',
                parentNavigatorKey: _rootNavigatorKey,
                builder: (context, state) => const ProfileScreen(),
              ),
            ],
          ),
        ],
      ),
    ],
  );

  static final _rootNavigatorKey = GlobalKey<NavigatorState>();

  /// 跳转到登录页
  static void goToLogin() {
    router.go(login);
  }

  /// 跳转到注册页
  static void goToRegister() {
    router.go(register);
  }

  /// 跳转到首页
  static void goToHome() {
    router.go(home);
  }

  /// 跳转到档案详情
  static void goToRecordDetail(String recordId) {
    router.go('$records/$recordId');
  }

  /// 跳转到上传页面
  static void goToUpload() {
    router.go('$records/upload');
  }
}
