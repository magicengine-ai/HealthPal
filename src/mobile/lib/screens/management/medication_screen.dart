import 'package:flutter/material.dart';

/// 用药管理页（占位）
class MedicationScreen extends StatelessWidget {
  const MedicationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('用药管理'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () {
              // TODO: 添加用药
            },
          ),
        ],
      ),
      body: const Center(child: Text('用药管理页面 - 待实现')),
    );
  }
}
