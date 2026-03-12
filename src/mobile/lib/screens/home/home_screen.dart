import 'package:flutter/material.dart';
import '../../config/theme.dart';

/// 首页（带底部导航栏）
class HomeScreen extends StatefulWidget {
  final Widget? child;

  const HomeScreen({super.key, this.child});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: widget.child ?? _buildBody(),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          setState(() {
            _currentIndex = index;
          });
          // TODO: 路由切换
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: '首页',
          ),
          NavigationDestination(
            icon: Icon(Icons.folder_outlined),
            selectedIcon: Icon(Icons.folder),
            label: '档案',
          ),
          NavigationDestination(
            icon: Icon(Icons.analytics_outlined),
            selectedIcon: Icon(Icons.analytics),
            label: '分析',
          ),
          NavigationDestination(
            icon: Icon(Icons.medication_outlined),
            selectedIcon: Icon(Icons.medication),
            label: '用药',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outlined),
            selectedIcon: Icon(Icons.person),
            label: '我的',
          ),
        ],
      ),
    );
  }

  Widget _buildBody() {
    switch (_currentIndex) {
      case 0:
        return _buildHomeTab();
      case 1:
        return Container(); // 档案页
      case 2:
        return Container(); // 分析页
      case 3:
        return Container(); // 用药页
      case 4:
        return Container(); // 我的页
      default:
        return _buildHomeTab();
    }
  }

  Widget _buildHomeTab() {
    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(AppTheme.spacingMedium),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 顶部卡片 - 健康评分
            _buildHealthScoreCard(),
            const SizedBox(height: AppTheme.spacingMedium),
            // 最近指标
            Text(
              '最近指标',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: AppTheme.spacingSmall),
            _buildIndicatorsRow(),
            const SizedBox(height: AppTheme.spacingMedium),
            // 今日提醒
            Text(
              '今日提醒',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: AppTheme.spacingSmall),
            _buildRemindersList(),
            const SizedBox(height: AppTheme.spacingMedium),
            // 快捷操作
            _buildQuickActions(),
          ],
        ),
      ),
    );
  }

  Widget _buildHealthScoreCard() {
    return Container(
      padding: const EdgeInsets.all(AppTheme.spacingLarge),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppTheme.primaryBlue, Color(0xFF096DD9)],
        ),
        borderRadius: BorderRadius.circular(AppTheme.borderRadiusLarge),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '健康评分',
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.8),
                      fontSize: AppTheme.textSizeMedium,
                    ),
                  ),
                  const SizedBox(height: 4),
                  const Text(
                    '85',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 48,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 8,
                ),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: const Text(
                  '良好',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: AppTheme.textSizeMedium,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppTheme.spacingMedium),
          // 进度条
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: const LinearProgressIndicator(
              value: 0.85,
              backgroundColor: Colors.white24,
              valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
              minHeight: 8,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildIndicatorsRow() {
    return Row(
      children: [
        _buildIndicatorCard('血压', '120/80', '正常', Colors.blue),
        const SizedBox(width: AppTheme.spacingSmall),
        _buildIndicatorCard('血糖', '5.6', '正常', Colors.green),
        const SizedBox(width: AppTheme.spacingSmall),
        _buildIndicatorCard('体重', '65kg', '正常', Colors.orange),
      ],
    );
  }

  Widget _buildIndicatorCard(String label, String value, String status, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(AppTheme.spacingMedium),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(AppTheme.borderRadiusMedium),
          boxShadow: AppTheme.cardShadow,
        ),
        child: Column(
          children: [
            Text(
              label,
              style: TextStyle(
                color: AppTheme.textHint,
                fontSize: AppTheme.textSizeSmall,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              value,
              style: TextStyle(
                color: color,
                fontSize: AppTheme.textSizeLarge,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              status,
              style: TextStyle(
                color: color,
                fontSize: AppTheme.textSizeSmall,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRemindersList() {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(AppTheme.borderRadiusMedium),
        boxShadow: AppTheme.cardShadow,
      ),
      child: Column(
        children: [
          _buildReminderItem('08:00', '阿司匹林', '100mg', true),
          const Divider(height: 1),
          _buildReminderItem('12:00', '午餐后测血糖', '', false),
          const Divider(height: 1),
          _buildReminderItem('20:00', '运动', '30 分钟', false),
        ],
      ),
    );
  }

  Widget _buildReminderItem(String time, String title, String subtitle, bool taken) {
    return ListTile(
      leading: Container(
        width: 40,
        height: 40,
        decoration: BoxDecoration(
          color: taken ? AppTheme.successGreen.withOpacity(0.1) : AppTheme.primaryBlue.withOpacity(0.1),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Icon(
          taken ? Icons.check_circle : Icons.access_time,
          color: taken ? AppTheme.successGreen : AppTheme.primaryBlue,
        ),
      ),
      title: Text(
        title,
        style: TextStyle(
          decoration: taken ? TextDecoration.lineThrough : null,
          color: taken ? AppTheme.textHint : AppTheme.textPrimary,
        ),
      ),
      subtitle: subtitle.isNotEmpty ? Text(subtitle) : null,
      trailing: Text(
        time,
        style: TextStyle(
          color: AppTheme.textHint,
          fontSize: AppTheme.textSizeSmall,
        ),
      ),
    );
  }

  Widget _buildQuickActions() {
    return Row(
      children: [
        Expanded(
          child: ElevatedButton.icon(
            onPressed: () {
              // TODO: 跳转到上传页面
            },
            icon: const Icon(Icons.camera_alt),
            label: const Text('上传档案'),
          ),
        ),
        const SizedBox(width: AppTheme.spacingSmall),
        Expanded(
          child: OutlinedButton.icon(
            onPressed: () {
              // TODO: 跳转到记录症状页面
            },
            icon: const Icon(Icons.edit),
            label: const Text('记录症状'),
          ),
        ),
      ],
    );
  }
}
