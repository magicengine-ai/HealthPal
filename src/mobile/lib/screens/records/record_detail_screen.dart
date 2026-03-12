import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../providers/records_provider.dart';
import '../../models/record_model.dart';

/// 档案详情页
class RecordDetailScreen extends StatefulWidget {
  final String recordId;

  const RecordDetailScreen({super.key, required this.recordId});

  @override
  State<RecordDetailScreen> createState() => _RecordDetailScreenState();
}

class _RecordDetailScreenState extends State<RecordDetailScreen> {
  RecordModel? _record;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadRecordDetail();
  }

  Future<void> _loadRecordDetail() async {
    setState(() => _isLoading = true);
    
    final provider = context.read<RecordsProvider>();
    _record = await provider.getRecordDetail(widget.recordId);
    
    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (_record == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('档案详情')),
        body: const Center(child: Text('档案不存在')),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(_record!.title),
        actions: [
          IconButton(
            icon: const Icon(Icons.more_vert),
            onPressed: () => _showMoreOptions(),
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _loadRecordDetail,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppTheme.spacingMedium),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 基本信息卡片
              _buildInfoCard(),
              const SizedBox(height: AppTheme.spacingMedium),
              
              // OCR 状态
              if (_record!.ocrStatus != 2) _buildOcrStatusCard(),
              
              // 指标列表
              if (_record!.indicators.isNotEmpty) ...[
                const SizedBox(height: AppTheme.spacingMedium),
                _buildIndicatorsSection(),
              ],
              
              // 文件列表
              if (_record!.files.isNotEmpty) ...[
                const SizedBox(height: AppTheme.spacingMedium),
                _buildFilesSection(),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildInfoCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppTheme.spacingMedium),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 标题
            Text(
              _record!.title,
              style: const TextStyle(
                fontSize: AppTheme.textSizeLarge,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: AppTheme.spacingSmall),
            
            // 类型标签
            Container(
              padding: const EdgeInsets.symmetric(
                horizontal: 12,
                vertical: 6,
              ),
              decoration: BoxDecoration(
                color: _getTypeColor(_record!.recordType).withOpacity(0.1),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                _record!.recordTypeText,
                style: TextStyle(
                  color: _getTypeColor(_record!.recordType),
                  fontSize: AppTheme.textSizeSmall,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ),
            const SizedBox(height: AppTheme.spacingMedium),
            
            // 详细信息
            _buildInfoRow(Icons.calendar_today, '检查日期', _record!.recordDate),
            const SizedBox(height: AppTheme.spacingSmall),
            _buildInfoRow(
              Icons.location_on,
              '医院',
              _record!.hospital ?? '未知',
            ),
            if (_record!.department != null) ...[
              const SizedBox(height: AppTheme.spacingSmall),
              _buildInfoRow(
                Icons.business,
                '科室',
                _record!.department!,
              ),
            ],
            const SizedBox(height: AppTheme.spacingSmall),
            _buildInfoRow(
              Icons.access_time,
              '创建时间',
              _formatDateTime(_record!.createdAt),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildOcrStatusCard() {
    return Card(
      color: AppTheme.warningOrange.withOpacity(0.1),
      child: Padding(
        padding: const EdgeInsets.all(AppTheme.spacingMedium),
        child: Row(
          children: [
            Icon(
              _record!.ocrStatus == 1 ? Icons.sync : Icons.error,
              color: AppTheme.warningOrange,
              size: 32,
            ),
            const SizedBox(width: AppTheme.spacingMedium),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    _record!.ocrStatus == 1 ? 'OCR 识别中' : 'OCR 识别失败',
                    style: const TextStyle(
                      fontSize: AppTheme.textSizeMedium,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  if (_record!.ocrMessage != null) ...[
                    const SizedBox(height: 4),
                    Text(
                      _record!.ocrMessage!,
                      style: TextStyle(
                        fontSize: AppTheme.textSizeSmall,
                        color: AppTheme.textHint,
                      ),
                    ),
                  ],
                ],
              ),
            ),
            if (_record!.ocrStatus == 1)
              const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(strokeWidth: 2),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildIndicatorsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              '健康指标 (${_record!.indicators.length}项)',
              style: const TextStyle(
                fontSize: AppTheme.textSizeMedium,
                fontWeight: FontWeight.bold,
              ),
            ),
            TextButton(
              onPressed: () {
                // TODO: 跳转到趋势分析
              },
              child: const Text('查看趋势'),
            ),
          ],
        ),
        const SizedBox(height: AppTheme.spacingSmall),
        ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: _record!.indicators.length,
          itemBuilder: (context, index) {
            final indicator = _record!.indicators[index];
            return Card(
              margin: const EdgeInsets.only(bottom: AppTheme.spacingSmall),
              child: ListTile(
                leading: Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: _getIndicatorStatusColor(indicator.status).withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    _getIndicatorStatusIcon(indicator.status),
                    color: _getIndicatorStatusColor(indicator.status),
                  ),
                ),
                title: Text(indicator.name),
                subtitle: indicator.referenceRange != null
                    ? Text('参考范围：${indicator.referenceRange}')
                    : null,
                trailing: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(
                      '${indicator.value} ${indicator.unit}',
                      style: TextStyle(
                        fontSize: AppTheme.textSizeMedium,
                        fontWeight: FontWeight.bold,
                        color: _getIndicatorStatusColor(indicator.status),
                      ),
                    ),
                    Text(
                      indicator.statusText,
                      style: TextStyle(
                        fontSize: AppTheme.textSizeSmall,
                        color: _getIndicatorStatusColor(indicator.status),
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ],
    );
  }

  Widget _buildFilesSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '原始文件 (${_record!.files.length}个)',
          style: const TextStyle(
            fontSize: AppTheme.textSizeMedium,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: AppTheme.spacingSmall),
        ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: _record!.files.length,
          itemBuilder: (context, index) {
            final file = _record!.files[index];
            return Card(
              child: ListTile(
                leading: const Icon(Icons.insert_drive_file),
                title: Text('文件 ${index + 1}'),
                subtitle: Text(_getFileName(file)),
                trailing: IconButton(
                  icon: const Icon(Icons.open_in_new),
                  onPressed: () {
                    // TODO: 打开文件
                  },
                ),
              ),
            );
          },
        ),
      ],
    );
  }

  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Row(
      children: [
        Icon(icon, size: 20, color: AppTheme.textHint),
        const SizedBox(width: 8),
        Text(
          '$label: ',
          style: TextStyle(color: AppTheme.textHint),
        ),
        Text(
          value,
          style: const TextStyle(fontWeight: FontWeight.w500),
        ),
      ],
    );
  }

  void _showMoreOptions() {
    showModalBottomSheet(
      context: context,
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.edit),
              title: const Text('编辑'),
              onTap: () {
                Navigator.pop(context);
                // TODO: 编辑档案
              },
            ),
            ListTile(
              leading: const Icon(Icons.share),
              title: const Text('分享'),
              onTap: () {
                Navigator.pop(context);
                // TODO: 分享档案
              },
            ),
            ListTile(
              leading: const Icon(Icons.download),
              title: const Text('下载'),
              onTap: () {
                Navigator.pop(context);
                // TODO: 下载档案
              },
            ),
            ListTile(
              leading: const Icon(Icons.delete, color: Colors.red),
              title: const Text('删除', style: TextStyle(color: Colors.red)),
              onTap: () {
                Navigator.pop(context);
                _confirmDelete();
              },
            ),
          ],
        ),
      ),
    );
  }

  void _confirmDelete() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('确认删除'),
        content: const Text('确定要删除这份档案吗？此操作不可恢复。'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('取消'),
          ),
          ElevatedButton(
            onPressed: () async {
              final provider = context.read<RecordsProvider>();
              await provider.deleteRecord(widget.recordId);
              if (context.mounted) {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('删除成功')),
                );
                Navigator.pop(context); // 返回档案列表
              }
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
            ),
            child: const Text('删除'),
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

  Color _getIndicatorStatusColor(String status) {
    switch (status) {
      case 'normal':
        return AppTheme.successGreen;
      case 'warning':
        return AppTheme.warningOrange;
      case 'critical':
        return AppTheme.errorRed;
      default:
        return Colors.grey;
    }
  }

  IconData _getIndicatorStatusIcon(String status) {
    switch (status) {
      case 'normal':
        return Icons.check_circle;
      case 'warning':
        return Icons.warning;
      case 'critical':
        return Icons.error;
      default:
        return Icons.help;
    }
  }

  String _getFileName(String url) {
    try {
      return url.split('/').last;
    } catch (e) {
      return '未知文件';
    }
  }

  String _formatDateTime(DateTime dateTime) {
    return '${dateTime.year}-${dateTime.month.toString().padLeft(2, '0')}-${dateTime.day.toString().padLeft(2, '0')} ${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
  }
}
