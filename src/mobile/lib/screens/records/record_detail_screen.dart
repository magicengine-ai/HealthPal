import 'package:flutter/material.dart';

/// 档案详情页（占位）
class RecordDetailScreen extends StatelessWidget {
  final String recordId;

  const RecordDetailScreen({super.key, required this.recordId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('档案详情')),
      body: Center(child: Text('档案详情：$recordId - 待实现')),
    );
  }
}
