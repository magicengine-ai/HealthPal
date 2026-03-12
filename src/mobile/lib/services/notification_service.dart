import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import '../utils/logger.dart';

/// 推送通知服务
class NotificationService {
  static final FlutterLocalNotificationsPlugin _notifications =
      FlutterLocalNotificationsPlugin();

  static bool _isInitialized = false;

  /// 初始化通知服务
  static Future<void> init() async {
    if (_isInitialized) return;

    // Android 初始化设置
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    
    // iOS 初始化设置
    const iosSettings = DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );

    const settings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );

    await _notifications.initialize(
      settings,
      onDidReceiveNotificationResponse: _onNotificationTapped,
    );

    // 创建通知渠道
    await _createNotificationChannels();
    
    _isInitialized = true;
    AppLogger.i('通知服务初始化完成');
  }

  /// 创建通知渠道
  static Future<void> _createNotificationChannels() async {
    const List<AndroidNotificationChannel> channels = [
      AndroidNotificationChannel(
        'medications',
        '用药提醒',
        description: '用药时间提醒',
        importance: Importance.high,
        playSound: true,
        enableVibration: true,
      ),
      AndroidNotificationChannel(
        'health_reports',
        '健康报告',
        description: '健康日报、周报',
        importance: Importance.defaultImportance,
      ),
      AndroidNotificationChannel(
        'appointments',
        '预约提醒',
        description: '就诊预约提醒',
        importance: Importance.high,
      ),
    ];

    for (var channel in channels) {
      await _notifications
          .resolvePlatformSpecificImplementation<
              AndroidFlutterLocalNotificationsPlugin>()
          ?.createNotificationChannel(channel);
    }
  }

  /// 通知点击回调
  static void _onNotificationTapped(NotificationResponse response) {
    AppLogger.i('通知被点击：${response.payload}');
    // TODO: 处理通知点击，跳转到对应页面
  }

  /// 显示用药提醒
  static Future<void> showMedicationReminder({
    required String title,
    required String body,
    String? medicineName,
    String? dosage,
  }) async {
    await _showNotification(
      id: DateTime.now().millisecondsSinceEpoch ~/ 1000,
      title: title,
      body: body,
      channelId: 'medications',
      payload: medicineName,
    );
  }

  /// 显示健康报告
  static Future<void> showHealthReport({
    required String title,
    required String body,
  }) async {
    await _showNotification(
      id: DateTime.now().millisecondsSinceEpoch ~/ 1000,
      title: title,
      body: body,
      channelId: 'health_reports',
    );
  }

  /// 显示预约提醒
  static Future<void> showAppointmentReminder({
    required String title,
    required String body,
  }) async {
    await _showNotification(
      id: DateTime.now().millisecondsSinceEpoch ~/ 1000,
      title: title,
      body: body,
      channelId: 'appointments',
    );
  }

  /// 显示通知
  static Future<void> _showNotification({
    required int id,
    required String title,
    required String body,
    required String channelId,
    String? payload,
  }) async {
    const androidDetails = AndroidNotificationDetails(
      'medications',
      '用药提醒',
      channelDescription: '用药时间提醒',
      importance: Importance.high,
      priority: Priority.high,
      icon: '@mipmap/ic_launcher',
      playSound: true,
      enableVibration: true,
    );

    const iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );

    const details = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _notifications.show(
      id,
      title,
      body,
      details,
      payload: payload,
    );

    AppLogger.d('通知已显示：$title');
  }

  /// 取消通知
  static Future<void> cancelNotification(int id) async {
    await _notifications.cancel(id);
  }

  /// 取消所有通知
  static Future<void> cancelAll() async {
    await _notifications.cancelAll();
  }

  /// 请求权限
  static Future<bool> requestPermissions() async {
    final androidPlugin = _notifications.resolvePlatformSpecificImplementation<
        AndroidFlutterLocalNotificationsPlugin>();
    
    final iosPlugin = _notifications.resolvePlatformSpecificImplementation<
        IOSFlutterLocalNotificationsPlugin>();

    bool? androidGranted;
    bool? iosGranted;

    if (androidPlugin != null) {
      androidGranted = await androidPlugin.requestNotificationsPermission();
    }

    if (iosPlugin != null) {
      iosGranted = await iosPlugin.requestPermissions(
        alert: true,
        badge: true,
        sound: true,
      );
    }

    return (androidGranted ?? true) && (iosGranted ?? true);
  }
}
