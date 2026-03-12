import 'package:flutter/material.dart';

/// 档案列表页（占位）
class RecordsScreen extends StatelessWidget {
  const RecordsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('健康档案'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () {
              // TODO: 跳转到上传页面
            },
          ),
        ],
      ),
      body: const Center(child: Text('档案列表页 - 待实现')),
    );
  }
}
