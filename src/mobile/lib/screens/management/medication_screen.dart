import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../providers/medication_provider.dart';
import '../../models/medication_model.dart';

/// 用药管理页
class MedicationScreen extends StatefulWidget {
  const MedicationScreen({super.key});

  @override
  State<MedicationScreen> createState() => _MedicationScreenState();
}

class _MedicationScreenState extends State<MedicationScreen> {
  @override
  void initState() {
    super.initState();
    _loadMedications();
  }

  Future<void> _loadMedications() async {
    final provider = context.read<MedicationProvider>();
    await provider.loadMedications();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('用药管理'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => _showAddMedicationDialog(),
            tooltip: '添加用药',
          ),
        ],
      ),
      body: Consumer<MedicationProvider>(
        builder: (context, provider, child) {
          if (provider.isLoading && provider.medications.isEmpty) {
            return const Center(child: CircularProgressIndicator());
          }

          if (provider.medications.isEmpty) {
            return _buildEmptyState();
          }

          return RefreshIndicator(
            onRefresh: _loadMedications,
            child: ListView(
              padding: const EdgeInsets.all(AppTheme.spacingMedium),
              children: [
                // 今日用药提醒
                if (provider.todayMedications.isNotEmpty) ...[
                  _buildTodayReminders(provider.todayMedications),
                  const SizedBox(height: AppTheme.spacingLarge),
                ],
                
                // 所有用药列表
                Text(
                  '所有用药',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: AppTheme.spacingSmall),
                ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: provider.medications.length,
                  itemBuilder: (context, index) {
                    final medication = provider.medications[index];
                    return _buildMedicationCard(medication);
                  },
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildTodayReminders(List<MedicationModel> medications) {
    return Card(
      color: AppTheme.primaryBlue.withOpacity(0.1),
      child: Padding(
        padding: const EdgeInsets.all(AppTheme.spacingMedium),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(
                  Icons.medication,
                  color: AppTheme.primaryBlue,
                ),
                const SizedBox(width: AppTheme.spacingSmall),
                Text(
                  '今日用药',
                  style: TextStyle(
                    fontSize: AppTheme.textSizeMedium,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.primaryBlue,
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppTheme.spacingMedium),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: medications.length,
              itemBuilder: (context, index) {
                final med = medications[index];
                return _buildReminderItem(med);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildReminderItem(MedicationModel med) {
    return Container(
      margin: const EdgeInsets.only(bottom: AppTheme.spacingSmall),
      padding: const EdgeInsets.all(AppTheme.spacingMedium),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(AppTheme.borderRadiusMedium),
      ),
      child: Row(
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              color: AppTheme.primaryBlue.withOpacity(0.1),
              borderRadius: BorderRadius.circular(24),
            ),
            child: const Icon(
              Icons.medication_outlined,
              color: AppTheme.primaryBlue,
            ),
          ),
          const SizedBox(width: AppTheme.spacingMedium),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  med.name,
                  style: const TextStyle(
                    fontSize: AppTheme.textSizeMedium,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '${med.dosage} · ${med.frequency}',
                  style: TextStyle(
                    fontSize: AppTheme.textSizeSmall,
                    color: AppTheme.textHint,
                  ),
                ),
              ],
            ),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                med.getNextDoseTime() ?? '--:--',
                style: TextStyle(
                  fontSize: AppTheme.textSizeMedium,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.primaryBlue,
                ),
              ),
              const SizedBox(height: 4),
              ElevatedButton(
                onPressed: () => _markAsTaken(med),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.successGreen,
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 8,
                  ),
                ),
                child: const Text('已服用'),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildMedicationCard(MedicationModel med) {
    return Card(
      margin: const EdgeInsets.only(bottom: AppTheme.spacingSmall),
      child: ListTile(
        leading: Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: _getStatusColor(med.status).withOpacity(0.1),
            borderRadius: BorderRadius.circular(24),
          ),
          child: Icon(
            Icons.medication_outlined,
            color: _getStatusColor(med.status),
          ),
        ),
        title: Text(
          med.name,
          style: const TextStyle(fontWeight: FontWeight.w500),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 4),
            Text('${med.dosage} · ${med.frequency}'),
            const SizedBox(height: 4),
            Row(
              children: [
                Icon(
                  Icons.access_time,
                  size: 14,
                  color: AppTheme.textHint,
                ),
                const SizedBox(width: 4),
                Text(
                  med.reminderTimes.join(', '),
                  style: TextStyle(
                    fontSize: AppTheme.textSizeSmall,
                    color: AppTheme.textHint,
                  ),
                ),
              ],
            ),
          ],
        ),
        trailing: PopupMenuButton(
          itemBuilder: (context) => [
            const PopupMenuItem(
              value: 'edit',
              child: Row(
                children: [
                  Icon(Icons.edit),
                  SizedBox(width: 8),
                  Text('编辑'),
                ],
              ),
            ),
            const PopupMenuItem(
              value: 'delete',
              child: Row(
                children: [
                  Icon(Icons.delete, color: Colors.red),
                  SizedBox(width: 8),
                  Text('删除', style: TextStyle(color: Colors.red)),
                ],
              ),
            ),
          ],
          onSelected: (value) {
            if (value == 'edit') {
              _showEditMedicationDialog(med);
            } else if (value == 'delete') {
              _confirmDelete(med);
            }
          },
        ),
        isThreeLine: true,
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.medication_outlined,
            size: 80,
            color: AppTheme.textHint,
          ),
          const SizedBox(height: AppTheme.spacingMedium),
          Text(
            '暂无用药记录',
            style: TextStyle(
              fontSize: AppTheme.textSizeLarge,
              color: AppTheme.textHint,
            ),
          ),
          const SizedBox(height: AppTheme.spacingSmall),
          Text(
          '点击右上角按钮添加第一个用药提醒',
            style: TextStyle(
              fontSize: AppTheme.textSizeSmall,
              color: AppTheme.textHint,
            ),
          ),
          const SizedBox(height: AppTheme.spacingLarge),
          ElevatedButton.icon(
            onPressed: () => _showAddMedicationDialog(),
            icon: const Icon(Icons.add),
            label: const Text('添加用药'),
          ),
        ],
      ),
    );
  }

  void _showAddMedicationDialog() {
    // TODO: 实现添加用药对话框
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('添加用药'),
        content: const Text('此功能待实现'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('确定'),
          ),
        ],
      ),
    );
  }

  void _showEditMedicationDialog(MedicationModel med) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('编辑 ${med.name}'),
        content: const Text('此功能待实现'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('取消'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('保存'),
          ),
        ],
      ),
    );
  }

  void _confirmDelete(MedicationModel med) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('确认删除'),
        content: Text('确定要删除"${med.name}"吗？'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('取消'),
          ),
          ElevatedButton(
            onPressed: () async {
              final provider = context.read<MedicationProvider>();
              await provider.deleteMedication(med.id);
              if (context.mounted) {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('删除成功')),
                );
              }
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('删除'),
          ),
        ],
      ),
    );
  }

  Future<void> _markAsTaken(MedicationModel med) async {
    final provider = context.read<MedicationProvider>();
    await provider.markAsTaken(med.id);
    
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('已标记为服用'),
          backgroundColor: Colors.green,
        ),
      );
    }
  }

  Color _getStatusColor(int status) {
    switch (status) {
      case 1:
        return AppTheme.primaryBlue;
      case 2:
        return AppTheme.successGreen;
      case 3:
        return Colors.grey;
      default:
        return Colors.grey;
    }
  }
}
