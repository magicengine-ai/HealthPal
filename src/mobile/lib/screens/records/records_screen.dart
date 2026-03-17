import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../providers/records_provider.dart';
import '../../models/record_model.dart';
import '../../config/routes.dart';

/// 档案列表页
class RecordsScreen extends StatefulWidget {
  const RecordsScreen({super.key});

  @override
  State<RecordsScreen> createState() => _RecordsScreenState();
}

class _RecordsScreenState extends State<RecordsScreen> {
  String? _selectedType;
  final List<String> _recordTypes = ['全部', '体检', '病历', '检查', '化验'];

  @override
  void initState() {
    super.initState();
    _loadRecords();
  }

  Future<void> _loadRecords() async {
    final provider = context.read<RecordsProvider>();
    await provider.loadRecords(
      recordType: _selectedType == '全部' ? null : _selectedType,
      refresh: true,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('健康档案'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add_a_photo),
            onPressed: () => AppRouter.goToUpload(),
            tooltip: '上传档案',
          ),
        ],
      ),
      body: Column(
        children: [
          // 分类筛选
          _buildFilterBar(),
          // 档案列表
          Expanded(
            child: Consumer<RecordsProvider>(
              builder: (context, provider, child) {
                if (provider.isLoading && provider.records.isEmpty) {
                  return const Center(child: CircularProgressIndicator());
                }
                
                if (provider.records.isEmpty) {
                  return _buildEmptyState();
                }

                return RefreshIndicator(
                  onRefresh: _loadRecords,
                  child: ListView.builder(
                    padding: const EdgeInsets.all(AppTheme.spacingMedium),
                    itemCount: provider.records.length + (provider.hasMore ? 1 : 0),
                    itemBuilder: (context, index) {
                      if (index == provider.records.length) {
                        // 加载更多
                        if (provider.isLoading) {
                          return const Padding(
                            padding: EdgeInsets.all(16.0),
                            child: Center(child: CircularProgressIndicator()),
                          );
                        }
                        // 加载更多
                        WidgetsBinding.instance.addPostFrameCallback((_) {
                          provider.loadMore();
                        });
                        return const SizedBox.shrink();
                      }
                      
                      final record = provider.records[index];
                      return _buildRecordCard(record);
                    },
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFilterBar() {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppTheme.spacingMedium,
        vertical: AppTheme.spacingSmall,
      ),
      color: Colors.white,
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: _recordTypes.map((type) {
            final isSelected = type == _selectedType || (type == '全部' && _selectedType == null);
            return Padding(
              padding: const EdgeInsets.only(right: AppTheme.spacingSmall),
              child: FilterChip(
                label: Text(type),
                selected: isSelected,
                onSelected: (selected) {
                  setState(() {
                    _selectedType = type == '全部' ? null : type;
                  });
                  _loadRecords();
                },
                backgroundColor: AppTheme.background,
                selectedColor: AppTheme.primaryBlue.withOpacity(0.2),
                checkmarkColor: AppTheme.primaryBlue,
              ),
            );
          }).toList(),
        ),
      ),
    );
  }

  Widget _buildRecordCard(RecordModel record) {
    return Card(
      margin: const EdgeInsets.only(bottom: AppTheme.spacingMedium),
      child: InkWell(
        onTap: () => AppRouter.goToRecordDetail( record.uuid),
        borderRadius: BorderRadius.circular(AppTheme.borderRadiusMedium),
        child: Padding(
          padding: const EdgeInsets.all(AppTheme.spacingMedium),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 标题和日期
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: _getTypeColor(record.recordType).withOpacity(0.1),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      record.recordTypeText,
                      style: TextStyle(
                        color: _getTypeColor(record.recordType),
                        fontSize: AppTheme.textSizeSmall,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                  const SizedBox(width: AppTheme.spacingSmall),
                  Expanded(
                    child: Text(
                      record.title,
                      style: const TextStyle(
                        fontSize: AppTheme.textSizeMedium,
                        fontWeight: FontWeight.w500,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: AppTheme.spacingSmall),
              
              // 医院和日期
              Row(
                children: [
                  Icon(
                    Icons.location_on_outlined,
                    size: 16,
                    color: AppTheme.textHint,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    record.hospital ?? '未知医院',
                    style: TextStyle(
                      fontSize: AppTheme.textSizeSmall,
                      color: AppTheme.textHint,
                    ),
                  ),
                  const Spacer(),
                  Icon(
                    Icons.calendar_today_outlined,
                    size: 16,
                    color: AppTheme.textHint,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    record.recordDate,
                    style: TextStyle(
                      fontSize: AppTheme.textSizeSmall,
                      color: AppTheme.textHint,
                    ),
                  ),
                ],
              ),
              
              const SizedBox(height: AppTheme.spacingSmall),
              
              // 指标数量和 OCR 状态
              Row(
                children: [
                  if (record.indicators.isNotEmpty) ...[
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: AppTheme.successGreen.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Row(
                        children: [
                          const Icon(
                            Icons.analytics_outlined,
                            size: 14,
                            color: AppTheme.successGreen,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            '${record.indicators.length}项指标',
                            style: const TextStyle(
                              fontSize: AppTheme.textSizeSmall,
                              color: AppTheme.successGreen,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: AppTheme.spacingSmall),
                  ],
                  
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: _getOcrStatusColor(record.ocrStatus).withOpacity(0.1),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          _getOcrStatusIcon(record.ocrStatus),
                          size: 14,
                          color: _getOcrStatusColor(record.ocrStatus),
                        ),
                        const SizedBox(width: 4),
                        Text(
                          record.ocrStatusText,
                          style: TextStyle(
                            fontSize: AppTheme.textSizeSmall,
                            color: _getOcrStatusColor(record.ocrStatus),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.folder_open_outlined,
            size: 80,
            color: AppTheme.textHint,
          ),
          const SizedBox(height: AppTheme.spacingMedium),
          Text(
            '暂无健康档案',
            style: TextStyle(
              fontSize: AppTheme.textSizeLarge,
              color: AppTheme.textHint,
            ),
          ),
          const SizedBox(height: AppTheme.spacingSmall),
          Text(
            '点击右上角按钮上传第一份档案',
            style: TextStyle(
              fontSize: AppTheme.textSizeSmall,
              color: AppTheme.textHint,
            ),
          ),
          const SizedBox(height: AppTheme.spacingLarge),
          ElevatedButton.icon(
            onPressed: () => AppRouter.goToUpload(),
            icon: const Icon(Icons.add_a_photo),
            label: const Text('上传档案'),
          ),
        ],
      ),
    );
  }

  Color _getTypeColor(String type) {
    switch (type) {
      case '体检':
        return Colors.blue;
      case '病历':
        return Colors.orange;
      case '检查':
        return Colors.green;
      case '化验':
        return Colors.purple;
      default:
        return Colors.grey;
    }
  }

  Color _getOcrStatusColor(int status) {
    switch (status) {
      case 0:
        return Colors.grey;
      case 1:
        return Colors.orange;
      case 2:
        return Colors.green;
      case 3:
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  IconData _getOcrStatusIcon(int status) {
    switch (status) {
      case 0:
        return Icons.schedule;
      case 1:
        return Icons.sync;
      case 2:
        return Icons.check_circle;
      case 3:
        return Icons.error;
      default:
        return Icons.help;
    }
  }
}
