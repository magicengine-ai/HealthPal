"""
通知相关异步任务
"""
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
from app.core.celery_config import celery_app
from app.db.mysql import get_db
from app.db.mongodb import get_mongodb
from app.services.medication_service import MedicationService
from app.services.user_service import UserService
from app.core.config import settings


@celery_app.task(bind=True)
def send_medication_reminder(self, user_id: str, medication_id: str, reminder_time: str):
    """
    发送单个用药提醒
    
    Args:
        user_id: 用户 ID
        medication_id: 药品 ID
        reminder_time: 提醒时间
    """
    try:
        db = next(get_db())
        db_client = asyncio.run(get_mongodb())
        
        med_service = MedicationService(db, db_client)
        user_service = UserService(db, db_client)
        
        # 获取药品信息
        medication = med_service.get_medication_by_id(medication_id)
        if not medication:
            return {'success': False, 'error': '药品不存在'}
        
        # 获取用户信息
        user = user_service.get_user_by_id(user_id)
        if not user:
            return {'success': False, 'error': '用户不存在'}
        
        # 构建提醒消息
        message = f"⏰ 用药提醒\n\n"
        message += f"药品：{medication.get('name')}\n"
        message += f"剂量：{medication.get('dosage')}\n"
        message += f"时间：{reminder_time}\n\n"
        message += f"请按时服药，保持健康！💊"
        
        # TODO: 发送推送通知（集成极光推送/个推）
        # await push_service.send_notification(user_id, message)
        
        # 记录提醒发送日志
        med_service.log_reminder_sent(medication_id, {
            'user_id': user_id,
            'sent_at': datetime.now().isoformat(),
            'message': message
        })
        
        return {
            'success': True,
            'user_id': user_id,
            'medication_id': medication_id,
            'message': '提醒已发送'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@celery_app.task
def send_medication_reminders():
    """
    批量发送用药提醒（定时任务：每 5 分钟执行一次）
    
    查询所有需要提醒的用药记录并发送通知
    """
    try:
        db = next(get_db())
        db_client = asyncio.run(get_mongodb())
        
        med_service = MedicationService(db, db_client)
        
        # 获取当前时间范围（前后 5 分钟）
        now = datetime.now()
        time_range_start = now - timedelta(minutes=5)
        time_range_end = now + timedelta(minutes=5)
        
        # 查询需要提醒的用药
        reminders = med_service.get_due_reminders(
            time_range_start.strftime('%H:%M'),
            time_range_end.strftime('%H:%M')
        )
        
        sent_count = 0
        failed_count = 0
        
        for reminder in reminders:
            # 异步发送提醒
            result = send_medication_reminder.delay(
                reminder['user_id'],
                reminder['medication_id'],
                reminder['reminder_time']
            )
            
            if result.get('success'):
                sent_count += 1
            else:
                failed_count += 1
        
        return {
            'success': True,
            'total': len(reminders),
            'sent': sent_count,
            'failed': failed_count,
            'message': f'已发送 {sent_count} 个提醒，{failed_count} 个失败'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@celery_app.task(bind=True)
def send_health_report(self, user_id: str, report_data: Dict):
    """
    发送健康报告给用户
    
    Args:
        user_id: 用户 ID
        report_data: 报告数据
    """
    try:
        db = next(get_db())
        db_client = asyncio.run(get_mongodb())
        
        user_service = UserService(db, db_client)
        
        # 获取用户信息
        user = user_service.get_user_by_id(user_id)
        if not user:
            return {'success': False, 'error': '用户不存在'}
        
        # 构建报告消息
        message = f"📊 健康日报\n\n"
        message += f"日期：{report_data.get('date', datetime.now().strftime('%Y-%m-%d'))}\n\n"
        
        if report_data.get('summary'):
            message += f"📝 健康总结:\n{report_data['summary']}\n\n"
        
        if report_data.get('indicators'):
            message += f"📈 关键指标:\n"
            for indicator in report_data['indicators']:
                status_icon = "✅" if indicator.get('status') == 'normal' else "⚠️"
                message += f"{status_icon} {indicator.get('name')}: {indicator.get('value')} {indicator.get('unit')}\n"
        
        message += f"\n查看详细报告请登录 HealthPal App"
        
        # TODO: 发送推送通知
        # await push_service.send_notification(user_id, message)
        
        return {
            'success': True,
            'user_id': user_id,
            'message': '健康报告已发送'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@celery_app.task(bind=True)
def send_appointment_reminder(self, user_id: str, appointment_id: str, appointment_time: str):
    """
    发送预约提醒
    
    Args:
        user_id: 用户 ID
        appointment_id: 预约 ID
        appointment_time: 预约时间
    """
    try:
        db = next(get_db())
        db_client = asyncio.run(get_mongodb())
        
        user_service = UserService(db, db_client)
        
        # 获取用户信息
        user = user_service.get_user_by_id(user_id)
        if not user:
            return {'success': False, 'error': '用户不存在'}
        
        # 构建提醒消息
        message = f"🏥 就诊提醒\n\n"
        message += f"预约时间：{appointment_time}\n\n"
        message += f"请提前 15 分钟到达医院，记得携带医保卡和相关检查报告。"
        
        # TODO: 发送推送通知
        # await push_service.send_notification(user_id, message)
        
        return {
            'success': True,
            'user_id': user_id,
            'appointment_id': appointment_id,
            'message': '预约提醒已发送'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@celery_app.task
def batch_send_notifications(user_ids: List[str], message: str, notification_type: str = "general"):
    """
    批量发送通知
    
    Args:
        user_ids: 用户 ID 列表
        message: 通知内容
        notification_type: 通知类型 (general/medication/appointment/report)
    """
    results = []
    
    for user_id in user_ids:
        # 根据通知类型路由到不同任务
        if notification_type == "medication":
            result = send_medication_reminder.delay(user_id, "", "")
        elif notification_type == "report":
            result = send_health_report.delay(user_id, {})
        else:
            # 通用通知
            result = {'success': True, 'user_id': user_id}
        
        results.append(result)
    
    success_count = sum(1 for r in results if r.get('success'))
    
    return {
        'success': True,
        'total': len(user_ids),
        'sent': success_count,
        'failed': len(user_ids) - success_count
    }
