import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../config/theme.dart';
import '../../providers/records_provider.dart';
import '../../models/record_model.dart';

/// 健康分析页
class AnalysisScreen extends StatefulWidget {
  const AnalysisScreen({super.key});

  @override
  State<AnalysisScreen> createState() => _AnalysisScreenState();
}

class _AnalysisScreenState extends State<AnalysisScreen> {
  int _selectedTab = 0;
  final List<String> _indicatorTypes = ['血压', '血糖', '体重', '心率'];
  String _selectedPeriod = '30 天';
  
  // 模拟数据
  final List<FlSpot> _bloodPressureData = [
    const FlSpot(0, 118),
    const FlSpot(1, 122),
    const FlSpot(2, 120),
    const FlSpot(3, 125),
    const FlSpot(4, 123),
    const FlSpot(5, 119),
    const FlSpot(6, 121),
  ];
  
  final List<FlSpot> _bloodSugarData = [
    const FlSpot(0, 5.2),
    const FlSpot(1, 5.5),
    const FlSpot(2, 5.3),
    const FlSpot(3, 5.8),
    const FlSpot(4, 5.6),
    const FlSpot(5, 5.4),
    const FlSpot(6, 5.5),
  ];
  
  final List<FlSpot> _weightData = [
    const FlSpot(0, 64.5),
    const FlSpot(1, 64.8),
    const FlSpot(2, 65.0),
    const FlSpot(3, 65.2),
    const FlSpot(4, 65.1),
    const FlSpot(5, 64.9),
    const FlSpot(6, 65.0),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('健康分析'),
        actions: [
          PopupMenuButton<String>(
            onSelected: (value) {
              setState(() => _selectedPeriod = value);
            },
            itemBuilder: (context) => [
              const PopupMenuItem(value: '7 天', child: Text('最近 7 天')),
              const PopupMenuItem(value: '30 天', child: Text('最近 30 天')),
              const PopupMenuItem(value: '90 天', child: Text('最近 90 天')),
            ],
          ),
        ],
      ),
      body: Column(
        children: [
          // 指标类型选择
          _buildIndicatorSelector(),
          // 图表区域
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(AppTheme.spacingMedium),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 趋势图表
                  _buildTrendChart(),
                  const SizedBox(height: AppTheme.spacingLarge),
                  
                  // 统计数据
                  _buildStatistics(),
                  const SizedBox(height: AppTheme.spacingLarge),
                  
                  // 健康建议
                  _buildHealthTips(),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildIndicatorSelector() {
    return Container(
      padding: const EdgeInsets.all(AppTheme.spacingMedium),
      color: Colors.white,
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: _indicatorTypes.asMap().entries.map((entry) {
            final index = entry.key;
            final type = entry.value;
            final isSelected = _selectedTab == index;
            
            return Padding(
              padding: const EdgeInsets.only(right: AppTheme.spacingSmall),
              child: ChoiceChip(
                label: Text(type),
                selected: isSelected,
                onSelected: (selected) {
                  if (selected) {
                    setState(() => _selectedTab = index);
                  }
                },
                selectedColor: AppTheme.primaryBlue,
                labelStyle: TextStyle(
                  color: isSelected ? Colors.white : AppTheme.textPrimary,
                ),
              ),
            );
          }).toList(),
        ),
      ),
    );
  }

  Widget _buildTrendChart() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppTheme.spacingMedium),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '${_indicatorTypes[_selectedTab]}趋势',
              style: const TextStyle(
                fontSize: AppTheme.textSizeMedium,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: AppTheme.spacingMedium),
            SizedBox(
              height: 200,
              child: LineChart(
                LineChartData(
                  gridData: FlGridData(
                    show: true,
                    drawVerticalLine: true,
                    horizontalInterval: _getHorizontalInterval(),
                    verticalInterval: 1,
                    getDrawingHorizontalLine: (value) {
                      return FlLine(
                        color: AppTheme.divider,
                        strokeWidth: 1,
                      );
                    },
                    getDrawingVerticalLine: (value) {
                      return FlLine(
                        color: AppTheme.divider,
                        strokeWidth: 1,
                      );
                    },
                  ),
                  titlesData: FlTitlesData(
                    show: true,
                    rightTitles: const AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    topTitles: const AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 40,
                        getTitlesWidget: (value, meta) {
                          return Text(
                            value.toString(),
                            style: TextStyle(
                              color: AppTheme.textHint,
                              fontSize: 10,
                            ),
                          );
                        },
                      ),
                    ),
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 30,
                        getTitlesWidget: (value, meta) {
                          const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
                          if (value.toInt() >= 0 && value.toInt() < days.length) {
                            return Text(
                              days[value.toInt()],
                              style: TextStyle(
                                color: AppTheme.textHint,
                                fontSize: 10,
                              ),
                            );
                          }
                          return const Text('');
                        },
                      ),
                    ),
                  ),
                  borderData: FlBorderData(show: false),
                  minX: 0,
                  maxX: 6,
                  minY: _getMinY(),
                  maxY: _getMaxY(),
                  lineBarsData: [
                    LineChartBarData(
                      spots: _getCurrentData(),
                      isCurved: true,
                      color: AppTheme.primaryBlue,
                      barWidth: 3,
                      isStrokeCapRound: true,
                      dotData: FlDotData(
                        show: true,
                        getDotPainter: (spot, percent, barData, index) {
                          return FlDotCirclePainter(
                            radius: 4,
                            color: Colors.white,
                            strokeWidth: 2,
                            strokeColor: AppTheme.primaryBlue,
                          );
                        },
                      ),
                      belowBarData: BarAreaData(
                        show: true,
                        gradient: LinearGradient(
                          colors: [
                            AppTheme.primaryBlue.withOpacity(0.3),
                            AppTheme.primaryBlue.withOpacity(0.0),
                          ],
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatistics() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppTheme.spacingMedium),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '统计数据',
              style: const TextStyle(
                fontSize: AppTheme.textSizeMedium,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: AppTheme.spacingMedium),
            Row(
              children: [
                Expanded(
                  child: _buildStatItem(
                    '平均值',
                    _getAverage().toStringAsFixed(1),
                    _getUnit(),
                    Colors.blue,
                  ),
                ),
                Expanded(
                  child: _buildStatItem(
                    '最高值',
                    _getMax().toStringAsFixed(1),
                    _getUnit(),
                    Colors.orange,
                  ),
                ),
                Expanded(
                  child: _buildStatItem(
                    '最低值',
                    _getMin().toStringAsFixed(1),
                    _getUnit(),
                    Colors.green,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatItem(String label, String value, String unit, Color color) {
    return Column(
      children: [
        Text(
          label,
          style: TextStyle(
            color: AppTheme.textHint,
            fontSize: AppTheme.textSizeSmall,
          ),
        ),
        const SizedBox(height: 4),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              value,
              style: TextStyle(
                color: color,
                fontSize: AppTheme.textSizeLarge,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(width: 4),
            Text(
              unit,
              style: TextStyle(
                color: AppTheme.textHint,
                fontSize: AppTheme.textSizeSmall,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildHealthTips() {
    return Card(
      color: AppTheme.lifeGreen.withOpacity(0.1),
      child: Padding(
        padding: const EdgeInsets.all(AppTheme.spacingMedium),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(
                  Icons.lightbulb_outline,
                  color: AppTheme.lifeGreen,
                ),
                const SizedBox(width: 8),
                Text(
                  '健康建议',
                  style: TextStyle(
                    fontSize: AppTheme.textSizeMedium,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.lifeGreen,
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppTheme.spacingSmall),
            Text(
              _getHealthTip(),
              style: const TextStyle(
                fontSize: AppTheme.textSizeNormal,
                height: 1.5,
              ),
            ),
          ],
        ),
      ),
    );
  }

  List<FlSpot> _getCurrentData() {
    switch (_selectedTab) {
      case 0: // 血压
        return _bloodPressureData;
      case 1: // 血糖
        return _bloodSugarData;
      case 2: // 体重
        return _weightData;
      default:
        return _bloodPressureData;
    }
  }

  double _getHorizontalInterval() {
    switch (_selectedTab) {
      case 0: // 血压
        return 20;
      case 1: // 血糖
        return 1;
      case 2: // 体重
        return 0.5;
      default:
        return 20;
    }
  }

  double _getMinY() {
    final data = _getCurrentData();
    return data.map((e) => e.y).reduce((a, b) => a < b ? a : b) - 5;
  }

  double _getMaxY() {
    final data = _getCurrentData();
    return data.map((e) => e.y).reduce((a, b) => a > b ? a : b) + 5;
  }

  double _getAverage() {
    final data = _getCurrentData();
    final sum = data.map((e) => e.y).reduce((a, b) => a + b);
    return sum / data.length;
  }

  double _getMax() {
    final data = _getCurrentData();
    return data.map((e) => e.y).reduce((a, b) => a > b ? a : b);
  }

  double _getMin() {
    final data = _getCurrentData();
    return data.map((e) => e.y).reduce((a, b) => a < b ? a : b);
  }

  String _getUnit() {
    switch (_selectedTab) {
      case 0: // 血压
        return 'mmHg';
      case 1: // 血糖
        return 'mmol/L';
      case 2: // 体重
        return 'kg';
      default:
        return '';
    }
  }

  String _getHealthTip() {
    switch (_selectedTab) {
      case 0:
        return '您的血压保持在正常范围内。建议继续保持规律作息，适量运动，低盐饮食，定期监测血压变化。';
      case 1:
        return '您的血糖水平稳定。建议控制糖分摄入，多吃蔬菜，适量运动，避免暴饮暴食。';
      case 2:
        return '您的体重在健康范围内。建议保持均衡饮食，规律运动，保持良好的生活习惯。';
      default:
        return '请继续保持健康的生活方式！';
    }
  }
}
