import 'package:flutter/material.dart';

/// 应用主题配置
class AppTheme {
  // 主色调
  static const Color primaryBlue = Color(0xFF1890FF);
  static const Color lifeGreen = Color(0xFF52C41A);

  // 辅助色
  static const Color warningOrange = Color(0xFFFA8C16);
  static const Color errorRed = Color(0xFFF5222D);
  static const Color successGreen = Color(0xFF73D13D);

  // 中性色
  static const Color textPrimary = Color(0xFF333333);
  static const Color textSecondary = Color(0xFF666666);
  static const Color textHint = Color(0xFF999999);
  static const Color divider = Color(0xFFE8E8E8);
  static const Color background = Color(0xFFF5F5F5);
  static const Color cardBackground = Color(0xFFFFFFFF);

  // 字体大小
  static const double textSizeSmall = 12.0;
  static const double textSizeNormal = 14.0;
  static const double textSizeMedium = 16.0;
  static const double textSizeLarge = 18.0;
  static const double textSizeXLarge = 24.0;

  // 字体粗细
  static const FontWeight fontWeightNormal = FontWeight.w400;
  static const FontWeight fontWeightMedium = FontWeight.w500;
  static const FontWeight fontWeightBold = FontWeight.w600;

  // 圆角
  static const double borderRadiusSmall = 4.0;
  static const double borderRadiusMedium = 8.0;
  static const double borderRadiusLarge = 12.0;
  static const double borderRadiusXLarge = 16.0;

  // 间距
  static const double spacingSmall = 8.0;
  static const double spacingNormal = 12.0;
  static const double spacingMedium = 16.0;
  static const double spacingLarge = 24.0;
  static const double spacingXLarge = 32.0;

  // 阴影
  static List<BoxShadow> get cardShadow => [
        BoxShadow(
          color: Colors.black.withOpacity(0.08),
          blurRadius: 8.0,
          offset: const Offset(0, 2),
        ),
      ];

  // 浅色主题
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      primaryColor: primaryBlue,
      scaffoldBackgroundColor: background,
      cardColor: cardBackground,
      dividerColor: divider,
      fontFamily: 'PingFang',
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: textSizeXLarge,
          fontWeight: fontWeightBold,
          color: textPrimary,
        ),
        displayMedium: TextStyle(
          fontSize: textSizeLarge,
          fontWeight: fontWeightMedium,
          color: textPrimary,
        ),
        displaySmall: TextStyle(
          fontSize: textSizeMedium,
          fontWeight: fontWeightNormal,
          color: textPrimary,
        ),
        bodyLarge: TextStyle(
          fontSize: textSizeMedium,
          fontWeight: fontWeightNormal,
          color: textSecondary,
        ),
        bodyMedium: TextStyle(
          fontSize: textSizeNormal,
          fontWeight: fontWeightNormal,
          color: textSecondary,
        ),
        bodySmall: TextStyle(
          fontSize: textSizeSmall,
          fontWeight: fontWeightNormal,
          color: textHint,
        ),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: cardBackground,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(
          fontSize: textSizeMedium,
          fontWeight: fontWeightBold,
          color: textPrimary,
        ),
        iconTheme: IconThemeData(
          color: textPrimary,
          size: 24.0,
        ),
      ),
      cardTheme: CardTheme(
        color: cardBackground,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(borderRadiusLarge),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryBlue,
          foregroundColor: Colors.white,
          elevation: 0,
          padding: const EdgeInsets.symmetric(
            horizontal: 24.0,
            vertical: 12.0,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(borderRadiusMedium),
          ),
          textStyle: const TextStyle(
            fontSize: textSizeMedium,
            fontWeight: fontWeightMedium,
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: cardBackground,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 16.0,
          vertical: 12.0,
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(borderRadiusMedium),
          borderSide: const BorderSide(color: divider),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(borderRadiusMedium),
          borderSide: const BorderSide(color: divider),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(borderRadiusMedium),
          borderSide: const BorderSide(color: primaryBlue, width: 2.0),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(borderRadiusMedium),
          borderSide: const BorderSide(color: errorRed),
        ),
      ),
    );
  }

  // 深色主题
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      primaryColor: primaryBlue,
      scaffoldBackgroundColor: const Color(0xFF1A1A1A),
      cardColor: const Color(0xFF2A2A2A),
      dividerColor: const Color(0xFF3A3A3A),
      fontFamily: 'PingFang',
      // 其他配置类似浅色主题...
    );
  }
}
