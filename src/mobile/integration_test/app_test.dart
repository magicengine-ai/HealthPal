import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:healthpal/main.dart' as app;
import 'package:healthpal/screens/auth/login_screen.dart';
import 'package:healthpal/screens/home/home_screen.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('HealthPal 集成测试', () {
    testWidgets('启动页 -> 登录页', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // 验证启动页显示
      expect(find.text('HealthPal'), findsOneWidget);
      expect(find.text('您的个人健康档案 AI 助手'), findsOneWidget);
    });

    testWidgets('登录流程', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // 等待启动页完成
      await tester.pump(const Duration(seconds: 3));
      await tester.pumpAndSettle();

      // 验证跳转到登录页
      expect(find.byType(LoginScreen), findsOneWidget);

      // 输入手机号
      final phoneField = find.byType(TextFormField).at(0);
      await tester.enterText(phoneField, '13800138000');

      // 输入密码
      final passwordField = find.byType(TextFormField).at(1);
      await tester.enterText(passwordField, 'test123456');

      // 点击登录
      final loginButton = find.text('登录');
      await tester.tap(loginButton);
      await tester.pumpAndSettle();

      // 验证登录成功（跳转到首页）
      expect(find.byType(HomeScreen), findsOneWidget);
    });
  });
}
