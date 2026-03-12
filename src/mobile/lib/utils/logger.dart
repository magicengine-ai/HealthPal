import 'package:logger/logger.dart';

/// 日志工具
class AppLogger {
  static final Logger _logger = Logger(
    printer: PrettyPrinter(
      methodCount: 2,
      errorMethodCount: 8,
      lineLength: 120,
      colors: true,
      printEmojis: true,
      printTime: true,
    ),
  );

  static void d(String message, {String? tag}) {
    _logger.d(message, tag: tag);
  }

  static void i(String message, {String? tag}) {
    _logger.i(message, tag: tag);
  }

  static void w(String message, {String? tag}) {
    _logger.w(message, tag: tag);
  }

  static void e(String message, {String? tag, dynamic error}) {
    _logger.e(message, tag: tag, error: error);
  }

  static void json(String message) {
    _logger.d(message);
  }
}
