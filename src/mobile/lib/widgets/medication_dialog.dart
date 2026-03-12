import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../providers/medication_provider.dart';
import '../../models/medication_model.dart';

/// 添加/编辑用药对话框
class MedicationDialog extends StatefulWidget {
  final MedicationModel? medication;

  const MedicationDialog({super.key, this.medication});

  @override
  State<MedicationDialog> createState() => _MedicationDialogState();
}

class _MedicationDialogState extends State<MedicationDialog> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _dosageController = TextEditingController();
  final _frequencyController = TextEditingController();
  final _notesController = TextEditingController();
  
  List<String> _reminderTimes = [];
  DateTime? _startDate;
  DateTime? _endDate;
  int _status = 1;

  @override
  void initState() {
    super.initState();
    if (widget.medication != null) {
      _nameController.text = widget.medication!.name;
      _dosageController.text = widget.medication!.dosage;
      _frequencyController.text = widget.medication!.frequency;
      _notesController.text = widget.medication!.notes ?? '';
      _reminderTimes = List.from(widget.medication!.reminderTimes);
      _startDate = widget.medication!.startDate != null
          ? DateTime.parse(widget.medication!.startDate!)
          : null;
      _endDate = widget.medication!.endDate != null
          ? DateTime.parse(widget.medication!.endDate!)
          : null;
      _status = widget.medication!.status;
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _dosageController.dispose();
    _frequencyController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _selectDate(bool isStart) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: isStart ? (_startDate ?? DateTime.now()) : (_endDate ?? DateTime.now()),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    
    if (picked != null) {
      setState(() {
        if (isStart) {
          _startDate = picked;
        } else {
          _endDate = picked;
        }
      });
    }
  }

  Future<void> _addReminderTime() async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
    );
    
    if (picked != null) {
      final time = '${picked.hour.toString().padLeft(2, '0')}:${picked.minute.toString().padLeft(2, '0')}';
      setState(() {
        if (!_reminderTimes.contains(time)) {
          _reminderTimes.add(time);
          _reminderTimes.sort();
        }
      });
    }
  }

  void _removeReminderTime(String time) {
    setState(() {
      _reminderTimes.remove(time);
    });
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    final provider = context.read<MedicationProvider>();
    
    final medication = MedicationModel(
      id: widget.medication?.id ?? '',
      name: _nameController.text.trim(),
      dosage: _dosageController.text.trim(),
      frequency: _frequencyController.text.trim(),
      reminderTimes: _reminderTimes,
      startDate: _startDate != null ? _formatDate(_startDate!) : null,
      endDate: _endDate != null ? _formatDate(_endDate!) : null,
      status: _status,
      notes: _notesController.text.trim(),
      createdAt: widget.medication?.createdAt ?? DateTime.now(),
    );

    bool success;
    if (widget.medication == null) {
      success = await provider.addMedication(medication);
    } else {
      success = await provider.updateMedication(medication);
    }

    if (context.mounted) {
      Navigator.pop(context);
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(widget.medication == null ? '添加成功' : '更新成功'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('操作失败，请重试'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.medication == null ? '添加用药' : '编辑用药'),
        actions: [
          TextButton(
            onPressed: _submit,
            child: const Text('保存'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(AppTheme.spacingMedium),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // 药品名称
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: '药品名称',
                  hintText: '例如：阿司匹林',
                  prefixIcon: Icon(Icons.medication),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '请输入药品名称';
                  }
                  return null;
                },
              ),
              const SizedBox(height: AppTheme.spacingMedium),
              
              // 剂量
              TextFormField(
                controller: _dosageController,
                decoration: const InputDecoration(
                  labelText: '剂量',
                  hintText: '例如：100mg',
                  prefixIcon: Icon(Icons.science),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '请输入剂量';
                  }
                  return null;
                },
              ),
              const SizedBox(height: AppTheme.spacingMedium),
              
              // 频率
              TextFormField(
                controller: _frequencyController,
                decoration: const InputDecoration(
                  labelText: '频率',
                  hintText: '例如：每日 1 次',
                  prefixIcon: Icons.repeat,
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '请输入频率';
                  }
                  return null;
                },
              ),
              const SizedBox(height: AppTheme.spacingMedium),
              
              // 提醒时间
              Text(
                '提醒时间',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: AppTheme.spacingSmall),
              Wrap(
                spacing: AppTheme.spacingSmall,
                runSpacing: AppTheme.spacingSmall,
                children: [
                  ..._reminderTimes.map((time) => Chip(
                    label: Text(time),
                    deleteIcon: const Icon(Icons.close, size: 18),
                    onDeleted: () => _removeReminderTime(time),
                  )),
                  Chip(
                    avatar: const Icon(Icons.add, size: 20),
                    label: const Text('添加时间'),
                    onPressed: _addReminderTime,
                  ),
                ],
              ),
              if (_reminderTimes.isEmpty)
                Padding(
                  padding: const EdgeInsets.only(top: AppTheme.spacingSmall),
                  child: Text(
                    '请至少添加一个提醒时间',
                    style: TextStyle(color: Colors.red[300], fontSize: 12),
                  ),
                ),
              const SizedBox(height: AppTheme.spacingMedium),
              
              // 开始日期
              ListTile(
                contentPadding: EdgeInsets.zero,
                leading: const Icon(Icons.calendar_today),
                title: const Text('开始日期'),
                subtitle: Text(_startDate != null ? _formatDate(_startDate!) : '未设置'),
                onTap: () => _selectDate(true),
              ),
              
              // 结束日期
              ListTile(
                contentPadding: EdgeInsets.zero,
                leading: const Icon(Icons.event),
                title: const Text('结束日期'),
                subtitle: Text(_endDate != null ? _formatDate(_endDate!) : '未设置'),
                onTap: () => _selectDate(false),
              ),
              const SizedBox(height: AppTheme.spacingMedium),
              
              // 备注
              TextFormField(
                controller: _notesController,
                decoration: const InputDecoration(
                  labelText: '备注',
                  hintText: '例如：饭后服用',
                  prefixIcon: Icon(Icons.note),
                  alignLabelWithHint: true,
                ),
                maxLines: 3,
              ),
              const SizedBox(height: AppTheme.spacingXLarge),
              
              // 保存按钮
              ElevatedButton(
                onPressed: _submit,
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  child: const Text('保存'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
  }
}
