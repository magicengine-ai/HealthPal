import 'package:flutter/material.dart';
import '../config/theme.dart';

/// 提醒列表项组件
class ReminderItemWidget extends StatelessWidget {
  final String time;
  final String title;
  final String? subtitle;
  final bool isTaken;
  final VoidCallback? onToggle;

  const ReminderItemWidget({
    super.key,
    required this.time,
    required this.title,
    this.subtitle,
    required this.isTaken,
    this.onToggle,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppTheme.spacingMedium),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(AppTheme.borderRadiusMedium),
        boxShadow: AppTheme.cardShadow,
      ),
      child: Row(
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              color: isTaken
                  ? AppTheme.successGreen.withOpacity(0.1)
                  : AppTheme.primaryBlue.withOpacity(0.1),
              borderRadius: BorderRadius.circular(24),
            ),
            child: Icon(
              isTaken ? Icons.check_circle : Icons.access_time,
              color: isTaken ? AppTheme.successGreen : AppTheme.primaryBlue,
            ),
          ),
          const SizedBox(width: AppTheme.spacingMedium),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: AppTheme.textSizeMedium,
                    fontWeight: FontWeight.w500,
                    decoration: isTaken ? TextDecoration.lineThrough : null,
                    color: isTaken ? AppTheme.textHint : AppTheme.textPrimary,
                  ),
                ),
                if (subtitle != null) ...[
                  const SizedBox(height: 4),
                  Text(
                    subtitle!,
                    style: TextStyle(
                      fontSize: AppTheme.textSizeSmall,
                      color: AppTheme.textHint,
                    ),
                  ),
                ],
              ],
            ),
          ),
          Column(
            children: [
              Text(
                time,
                style: TextStyle(
                  color: AppTheme.textHint,
                  fontSize: AppTheme.textSizeSmall,
                ),
              ),
              if (onToggle != null) ...[
                const SizedBox(height: 8),
                IconButton(
                  icon: Icon(
                    isTaken ? Icons.undo : Icons.check,
                    size: 20,
                  ),
                  onPressed: onToggle,
                  color: isTaken ? AppTheme.textHint : AppTheme.successGreen,
                ),
              ],
            ],
          ),
        ],
      ),
    );
  }
}
