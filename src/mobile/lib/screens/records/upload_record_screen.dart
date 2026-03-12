import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../../config/theme.dart';
import '../../providers/records_provider.dart';
import '../../config/routes.dart';

/// 上传档案页
class UploadRecordScreen extends StatefulWidget {
  const UploadRecordScreen({super.key});

  @override
  State<UploadRecordScreen> createState() => _UploadRecordScreenState();
}

class _UploadRecordScreenState extends State<UploadRecordScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _hospitalController = TextEditingController();
  final _departmentController = TextEditingController();
  
  String _selectedType = '体检';
  DateTime _selectedDate = DateTime.now();
  XFile? _selectedFile;
  bool _isUploading = false;
  String? _taskId;
  int _ocrStatus = 0;
  
  final List<String> _recordTypes = ['体检', '病历', '检查', '化验', '其他'];
  final ImagePicker _picker = ImagePicker();

  @override
  void dispose() {
    _titleController.dispose();
    _hospitalController.dispose();
    _departmentController.dispose();
    super.dispose();
  }

  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? image = await _picker.pickImage(
        source: source,
        maxWidth: 2048,
        maxHeight: 2048,
        imageQuality: 85,
      );
      
      if (image != null) {
        setState(() => _selectedFile = image);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('选择图片失败：$e')),
        );
      }
    }
  }

  Future<void> _selectDate() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime(2000),
      lastDate: DateTime.now(),
    );
    
    if (picked != null && picked != _selectedDate) {
      setState(() => _selectedDate = picked);
    }
  }

  Future<void> _uploadRecord() async {
    if (!_formKey.currentState!.validate()) return;
    if (_selectedFile == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('请选择要上传的文件')),
      );
      return;
    }

    setState(() => _isUploading = true);

    try {
      final provider = context.read<RecordsProvider>();
      
      // TODO: 实现真实的文件上传
      // final success = await provider.uploadRecord(
      //   filePath: _selectedFile!.path,
      //   recordType: _selectedType,
      //   title: _titleController.text,
      //   recordDate: _formatDate(_selectedDate),
      //   hospital: _hospitalController.text.isEmpty ? null : _hospitalController.text,
      //   department: _departmentController.text.isEmpty ? null : _departmentController.text,
      // );

      // 模拟上传
      await Future.delayed(const Duration(seconds: 2));
      final success = true;

      if (!mounted) return;

      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('上传成功！OCR 识别中...'),
            backgroundColor: Colors.green,
          ),
        );
        context.go(AppRouter.records);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('上传失败，请重试'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('上传失败：$e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isUploading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('上传档案'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(AppTheme.spacingMedium),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // 文件选择
              _buildFileSelector(),
              const SizedBox(height: AppTheme.spacingLarge),
              
              // 档案类型
              _buildRecordTypeSelector(),
              const SizedBox(height: AppTheme.spacingMedium),
              
              // 标题
              TextFormField(
                controller: _titleController,
                decoration: const InputDecoration(
                  labelText: '档案标题',
                  hintText: '例如：2026 年年度体检',
                  prefixIcon: Icon(Icons.title),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '请输入档案标题';
                  }
                  return null;
                },
              ),
              const SizedBox(height: AppTheme.spacingMedium),
              
              // 检查日期
              InkWell(
                onTap: _selectDate,
                child: InputDecorator(
                  decoration: const InputDecoration(
                    labelText: '检查日期',
                    prefixIcon: Icon(Icons.calendar_today),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(_formatDate(_selectedDate)),
                      const Icon(Icons.arrow_drop_down),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: AppTheme.spacingMedium),
              
              // 医院
              TextFormField(
                controller: _hospitalController,
                decoration: const InputDecoration(
                  labelText: '医院名称',
                  hintText: '例如：北京协和医院',
                  prefixIcon: Icon(Icons.location_on),
                ),
              ),
              const SizedBox(height: AppTheme.spacingMedium),
              
              // 科室
              TextFormField(
                controller: _departmentController,
                decoration: const InputDecoration(
                  labelText: '科室',
                  hintText: '例如：体检中心',
                  prefixIcon: Icon(Icons.business),
                ),
              ),
              const SizedBox(height: AppTheme.spacingXLarge),
              
              // 上传按钮
              ElevatedButton(
                onPressed: _isUploading ? null : _uploadRecord,
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  child: _isUploading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                          ),
                        )
                      : const Text('上传档案'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFileSelector() {
    return GestureDetector(
      onTap: _showImageSourceDialog,
      child: Container(
        height: 200,
        decoration: BoxDecoration(
          color: AppTheme.background,
          borderRadius: BorderRadius.circular(AppTheme.borderRadiusLarge),
          border: Border.all(
            color: _selectedFile != null ? AppTheme.primaryBlue : AppTheme.divider,
            width: 2,
          ),
        ),
        child: _selectedFile == null
            ? _buildEmptyFileSelector()
            : _buildSelectedFilePreview(),
      ),
    );
  }

  Widget _buildEmptyFileSelector() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(
          Icons.add_photo_alternate_outlined,
          size: 64,
          color: AppTheme.textHint,
        ),
        const SizedBox(height: AppTheme.spacingMedium),
        Text(
          '点击拍照或选择图片',
          style: TextStyle(
            fontSize: AppTheme.textSizeMedium,
            color: AppTheme.textHint,
          ),
        ),
        const SizedBox(height: AppTheme.spacingSmall),
        Text(
          '支持 JPG、PNG、PDF 格式',
          style: TextStyle(
            fontSize: AppTheme.textSizeSmall,
            color: AppTheme.textHint,
          ),
        ),
      ],
    );
  }

  Widget _buildSelectedFilePreview() {
    return Stack(
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(AppTheme.borderRadiusLarge),
          child: Image.file(
            File(_selectedFile!.path),
            fit: BoxFit.cover,
            width: double.infinity,
            height: double.infinity,
          ),
        ),
        Positioned(
          top: 8,
          right: 8,
          child: IconButton(
            icon: const Icon(Icons.close, color: Colors.white),
            onPressed: () => setState(() => _selectedFile = null),
          ),
        ),
        Positioned(
          bottom: 8,
          left: 8,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.black54,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.check_circle, color: Colors.white, size: 16),
                const SizedBox(width: 4),
                const Text(
                  '已选择',
                  style: TextStyle(color: Colors.white, fontSize: 12),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildRecordTypeSelector() {
    return Wrap(
      spacing: AppTheme.spacingSmall,
      runSpacing: AppTheme.spacingSmall,
      children: _recordTypes.map((type) {
        final isSelected = type == _selectedType;
        return ChoiceChip(
          label: Text(type),
          selected: isSelected,
          onSelected: (selected) {
            if (selected) {
              setState(() => _selectedType = type);
            }
          },
          selectedColor: AppTheme.primaryBlue,
          labelStyle: TextStyle(
            color: isSelected ? Colors.white : AppTheme.textPrimary,
          ),
        );
      }).toList(),
    );
  }

  void _showImageSourceDialog() {
    showModalBottomSheet(
      context: context,
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt),
              title: const Text('拍照'),
              onTap: () {
                Navigator.pop(context);
                _pickImage(ImageSource.camera);
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library),
              title: const Text('从相册选择'),
              onTap: () {
                Navigator.pop(context);
                _pickImage(ImageSource.gallery);
              },
            ),
          ],
        ),
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
  }
}
