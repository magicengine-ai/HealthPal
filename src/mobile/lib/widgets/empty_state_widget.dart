import 'package:flutter/material.dart';
import '../config/theme.dart';

/// 空状态组件
class EmptyStateWidget extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final String? actionLabel;
  final VoidCallback? onAction;

  const EmptyStateWidget({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
    this.actionLabel,
    this.onAction,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            icon,
            size: 80,
            color: AppTheme.textHint,
          ),
          const SizedBox(height: AppTheme.spacingMedium),
          Text(
            title,
            style: TextStyle(
              fontSize: AppTheme.textSizeLarge,
              color: AppTheme.textHint,
            ),
          ),
          const SizedBox(height: AppTheme.spacingSmall),
          Text(
            subtitle,
            style: TextStyle(
              fontSize: AppTheme.textSizeSmall,
              color: AppTheme.textHint,
            ),
            textAlign: TextAlign.center,
          ),
          if (actionLabel != null && onAction != null) ...[
            const SizedBox(height: AppTheme.spacingLarge),
            ElevatedButton.icon(
              onPressed: onAction,
              icon: const Icon(Icons.add),
              label: Text(actionLabel!),
            ),
          ],
        ],
      ),
    );
  }
}
