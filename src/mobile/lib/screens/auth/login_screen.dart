import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/routes.dart';
import '../../providers/user_provider.dart';
import '../../config/theme.dart';

/// 登录页
class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _phoneController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _phoneController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (!_formKey.currentState!.validate()) return;

    final userProvider = context.read<UserProvider>();
    final success = await userProvider.login(
      _phoneController.text.trim(),
      _passwordController.text,
    );

    if (!mounted) return;

    if (success) {
      AppRouter.goToHome();
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('登录失败，请检查手机号和密码')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('登录'),
        actions: [
          TextButton(
            onPressed: () => AppRouter.goToRegister(),
            child: const Text('注册'),
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppTheme.spacingLarge),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: AppTheme.spacingXLarge),
                // Logo
                Icon(
                  Icons.favorite,
                  size: 80,
                  color: AppTheme.primaryBlue,
                ),
                const SizedBox(height: AppTheme.spacingMedium),
                Text(
                  '欢迎回来',
                  style: Theme.of(context).textTheme.displayMedium,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: AppTheme.spacingXLarge),
                // 手机号输入
                TextFormField(
                  controller: _phoneController,
                  keyboardType: TextInputType.phone,
                  decoration: const InputDecoration(
                    labelText: '手机号',
                    prefixIcon: Icon(Icons.phone_outlined),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return '请输入手机号';
                    }
                    if (!RegExp(r'^1[3-9]\d{9}$').hasMatch(value)) {
                      return '请输入正确的手机号';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: AppTheme.spacingMedium),
                // 密码输入
                TextFormField(
                  controller: _passwordController,
                  obscureText: _obscurePassword,
                  decoration: InputDecoration(
                    labelText: '密码',
                    prefixIcon: const Icon(Icons.lock_outlined),
                    suffixIcon: IconButton(
                      icon: Icon(
                        _obscurePassword
                            ? Icons.visibility_outlined
                            : Icons.visibility_off_outlined,
                      ),
                      onPressed: () {
                        setState(() {
                          _obscurePassword = !_obscurePassword;
                        });
                      },
                    ),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return '请输入密码';
                    }
                    if (value.length < 6) {
                      return '密码长度至少 6 位';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: AppTheme.spacingMedium),
                // 忘记密码
                Align(
                  alignment: Alignment.centerRight,
                  child: TextButton(
                    onPressed: () {
                      // TODO: 跳转到忘记密码页面
                    },
                    child: const Text('忘记密码？'),
                  ),
                ),
                const SizedBox(height: AppTheme.spacingLarge),
                // 登录按钮
                Consumer<UserProvider>(
                  builder: (context, provider, child) {
                    return ElevatedButton(
                      onPressed: provider.isLoading ? null : _handleLogin,
                      child: Padding(
                        padding: const EdgeInsets.symmetric(
                          vertical: AppTheme.spacingNormal,
                        ),
                        child: provider.isLoading
                            ? const SizedBox(
                                height: 20,
                                width: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor:
                                      AlwaysStoppedAnimation<Color>(Colors.white),
                                ),
                              )
                            : const Text('登录'),
                      ),
                    );
                  },
                ),
                const SizedBox(height: AppTheme.spacingLarge),
                // 分隔线
                Row(
                  children: [
                    const Expanded(child: Divider()),
                    Padding(
                      padding: const EdgeInsets.symmetric(
                        horizontal: AppTheme.spacingMedium,
                      ),
                      child: Text(
                        '其他登录方式',
                        style: TextStyle(color: AppTheme.textHint),
                      ),
                    ),
                    const Expanded(child: Divider()),
                  ],
                ),
                const SizedBox(height: AppTheme.spacingLarge),
                // 第三方登录
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _buildThirdPartyLogin(Icons.wechat, Colors.green),
                    const SizedBox(width: AppTheme.spacingXLarge),
                    _buildThirdPartyLogin(Icons.facebook, Colors.blue),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildThirdPartyLogin(IconData icon, Color color) {
    return InkWell(
      onTap: () {
        // TODO: 第三方登录
      },
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(50),
        ),
        child: Icon(icon, color: color, size: 32),
      ),
    );
  }
}
