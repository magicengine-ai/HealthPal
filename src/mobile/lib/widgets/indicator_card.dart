import 'package:flutter/material.dart';
import '../config/theme.dart';

/// 指标卡片组件
class IndicatorCard extends StatelessWidget {
  final String label;
  final String value;
  final String unit;
  final String status;
  final Color? color;

  const IndicatorCard({
    super.key,
    required this.label,
    required this.value,
    required this.unit,
    required this.status,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    final statusColor = _getStatusColor();
    
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
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  value,
                  style: TextStyle(
                    color: statusColor,
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
            const SizedBox(height: 4),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: BoxDecoration(
                color: statusColor.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                _getStatusText(),
                style: TextStyle(
                  color: statusColor,
                  fontSize: AppTheme.textSizeSmall,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Color _getStatusColor() {
    if (color != null) return color!;
    
    switch (status.toLowerCase()) {
      case 'normal':
        return AppTheme.successGreen;
      case 'warning':
        return AppTheme.warningOrange;
      case 'critical':
        return AppTheme.errorRed;
      default:
        return AppTheme.primaryBlue;
    }
  }

  String _getStatusText() {
    switch (status.toLowerCase()) {
      case 'normal':
        return '正常';
      case 'warning':
        return '异常';
      case 'critical':
        return '危急';
      default:
        return status;
    }
  }
}
