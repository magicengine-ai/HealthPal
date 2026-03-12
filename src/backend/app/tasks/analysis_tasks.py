"""
健康数据分析相关异步任务
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List
from app.core.celery_config import celery_app
from app.db.mysql import get_db
from app.db.mongodb import get_mongodb
from app.services.record_service import RecordService
from app.services.indicator_service import IndicatorService
from app.services.user_service import UserService
from app.tasks.notification_tasks import send_health_report


@celery_app.task(bind=True)
def analyze_health_indicators(self, user_id: str, days: int = 30):
    """
    分析用户健康指标趋势
    
    Args:
        user_id: 用户 ID
        days: 分析天数，默认 30 天
    """
    try:
        db = next(get_db())
        db_client = asyncio.run(get_mongodb())
        
        indicator_service = IndicatorService(db, db_client)
        record_service = RecordService(db, db_client)
        
        # 获取时间范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取用户指标数据
        indicators = indicator_service.get_user_indicators(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # 分析趋势
        analysis_result = {
            'user_id': user_id,
            'period': f'{start_date.strftime("%Y-%m-%d")} ~ {end_date.strftime("%Y-%m-%d")}',
            'indicators': []
        }
        
        for indicator_data in indicators:
            values = indicator_data.get('values', [])
            if len(values) < 2:
                continue
            
            # 计算趋势
            first_value = values[0].get('value', 0)
            last_value = values[-1].get('value', 0)
            change = last_value - first_value
            change_percent = (change / first_value * 100) if first_value != 0 else 0
            
            # 判断趋势
            trend = "stable"
            if abs(change_percent) > 5:
                trend = "up" if change > 0 else "down"
            
            analysis_result['indicators'].append({
                'name': indicator_data.get('name'),
                'unit': indicator_data.get('unit'),
                'current': last_value,
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'trend': trend,
                'status': indicator_data.get('status', 'unknown')
            })
        
        # 保存分析结果
        indicator_service.save_analysis(user_id, analysis_result)
        
        return {
            'success': True,
            'user_id': user_id,
            'indicators_analyzed': len(analysis_result['indicators']),
            'analysis': analysis_result
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@celery_app.task(bind=True)
def generate_daily_health_report(self, user_id: str = None):
    """
    生成健康日报（定时任务：每天早上 8 点执行）
    
    Args:
        user_id: 可选，指定用户；不传则生成所有用户的报告
    """
    try:
        db = next(get_db())
        db_client = asyncio.run(get_mongodb())
        
        user_service = UserService(db, db_client)
        indicator_service = IndicatorService(db, db_client)
        record_service = RecordService(db, db_client)
        
        # 如果指定了用户 ID，只生成该用户的报告
        if user_id:
            user_ids = [user_id]
        else:
            # 获取所有活跃用户
            users = user_service.get_all_active_users()
            user_ids = [u['id'] for u in users]
        
        reports_generated = 0
        
        for uid in user_ids:
            # 获取用户信息
            user = user_service.get_user_by_id(uid)
            if not user:
                continue
            
            # 获取昨日指标数据
            yesterday = datetime.now() - timedelta(days=1)
            indicators = indicator_service.get_user_indicators(
                user_id=uid,
                start_date=yesterday - timedelta(hours=12),
                end_date=yesterday + timedelta(hours=12)
            )
            
            # 获取健康总结
            summary = self._generate_health_summary(indicators)
            
            # 构建报告数据
            report_data = {
                'date': yesterday.strftime('%Y-%m-%d'),
                'summary': summary,
                'indicators': [
                    {
                        'name': ind.get('name'),
                        'value': ind.get('values', [{}])[-1].get('value', 0),
                        'unit': ind.get('unit', ''),
                        'status': ind.get('status', 'unknown')
                    }
                    for ind in indicators[:5]  # 最多 5 个指标
                ]
            }
            
            # 异步发送报告
            send_health_report.delay(uid, report_data)
            reports_generated += 1
        
        return {
            'success': True,
            'reports_generated': reports_generated,
            'message': f'已生成 {reports_generated} 份健康日报'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
    
    def _generate_health_summary(self, indicators: List[Dict]) -> str:
        """生成健康总结文本"""
        if not indicators:
            return "暂无足够数据生成健康总结"
        
        abnormal_count = sum(1 for ind in indicators if ind.get('status') != 'normal')
        
        if abnormal_count == 0:
            return "🎉 您的各项指标都在正常范围内，继续保持！"
        elif abnormal_count <= 2:
            return f"⚠️ 发现 {abnormal_count} 项指标异常，建议关注并适时复查。"
        else:
            return f"🚨 发现 {abnormal_count} 项指标异常，建议尽快就医咨询。"


@celery_app.task(bind=True)
def daily_health_backup(self):
    """
    每日健康数据备份（定时任务：每天凌晨 2 点执行）
    
    备份用户健康数据到 MongoDB 归档集合
    """
    try:
        db = next(get_db())
        db_client = asyncio.run(get_mongodb())
        
        record_service = RecordService(db, db_client)
        
        # 获取昨天的日期
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime('%Y-%m-%d')
        
        # 备份健康档案
        records = record_service.get_all_records_by_date(yesterday)
        
        backup_result = {
            'backup_date': date_str,
            'records_count': len(records),
            'status': 'completed'
        }
        
        # 保存到备份集合
        db_client['healthpal_backup'][f'records_{date_str}'].insert_many(records)
        
        return {
            'success': True,
            'backup': backup_result,
            'message': f'已备份 {len(records)} 条档案记录'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@celery_app.task(bind=True)
def detect_abnormal_indicators(self, user_id: str):
    """
    检测用户异常指标并告警
    
    Args:
        user_id: 用户 ID
    """
    try:
        db = next(get_db())
        db_client = asyncio.run(get_mongodb())
        
        indicator_service = IndicatorService(db, db_client)
        
        # 获取用户最新指标
        indicators = indicator_service.get_user_latest_indicators(user_id)
        
        alerts = []
        
        for indicator in indicators:
            status = indicator.get('status', 'normal')
            
            if status == 'critical':
                alerts.append({
                    'level': 'critical',
                    'indicator': indicator.get('name'),
                    'value': indicator.get('values', [{}])[-1].get('value'),
                    'message': f"⚠️ {indicator.get('name')} 异常，请立即就医！"
                })
            elif status == 'warning':
                alerts.append({
                    'level': 'warning',
                    'indicator': indicator.get('name'),
                    'value': indicator.get('values', [{}])[-1].get('value'),
                    'message': f"⚠️ {indicator.get('name')} 偏高/偏低，请注意观察"
                })
        
        if alerts:
            # TODO: 发送紧急通知
            # send_urgent_alert.delay(user_id, alerts)
            pass
        
        return {
            'success': True,
            'user_id': user_id,
            'alerts_count': len(alerts),
            'alerts': alerts
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@celery_app.task
def batch_analyze_users(user_ids: List[str], days: int = 30):
    """
    批量分析用户健康数据
    
    Args:
        user_ids: 用户 ID 列表
        days: 分析天数
    """
    results = []
    
    for user_id in user_ids:
        result = analyze_health_indicators.delay(user_id, days)
        results.append({
            'user_id': user_id,
            'task_id': result.id
        })
    
    return {
        'success': True,
        'total': len(user_ids),
        'tasks': results
    }
