from apscheduler.schedulers.background import BackgroundScheduler
from app.services.order_notification_services import OrderNotificationService
from datetime import datetime

class OrderNotificationScheduler:
    
    _scheduler = None
    
    @staticmethod
    def init_scheduler(app):
        """Khởi tạo scheduler để gửi email định kỳ"""
        
        if OrderNotificationScheduler._scheduler is not None:
            return 
        
        scheduler = BackgroundScheduler()
        
        scheduler.add_job(
            func=lambda: OrderNotificationScheduler._send_notifications_with_app_context(app),
            trigger='cron',
            hour=20,         # ← 20h tối
            minute=0,        # ← 0 phút
            id='order_notification_job',
            name='Send daily order report to managers at 20:00',
            replace_existing=True
        )
        
        # scheduler.add_job(
        #     func=lambda: OrderNotificationScheduler._send_notifications_with_app_context(app),
        #     trigger='interval',
        #     seconds=20,
        #     id='test_order_report_5s',
        #     name='[TEST] Send order report every 5 seconds',
        #     replace_existing=True
        # )
        
        scheduler.start()
        OrderNotificationScheduler._scheduler = scheduler
        
        print('Scheduler đã khởi động: Gửi email manager lúc 20:00 mỗi ngày')
        
        import atexit
        atexit.register(lambda: scheduler.shutdown())
    
    @staticmethod
    def _send_notifications_with_app_context(app):
        """Wrapper để chạy với Flask app context"""
        with app.app_context():
            OrderNotificationService.send_daily_report_to_managers()