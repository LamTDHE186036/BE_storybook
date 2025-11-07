from app.extension import db
from app.models.order import Order
from app.models.users import User
from app.services.otp_mail_services import EmailService
from datetime import datetime, timezone, timedelta


class OrderNotificationService:
    
    @staticmethod
    def get_orders_last_24h():
        """Lấy đơn hàng từ 20:00 hôm qua đến 20:00 hôm nay"""
        try:
            # Lấy thời gian hiện tại
            now = datetime.now(timezone.utc)
            
            # Lấy thời gian 20:00 hôm qua
            yesterday_20h = now.replace(hour=20, minute=0, second=0, microsecond=0) - timedelta(days=1)
            
            # Lấy thời gian 20:00 hôm nay
            today_20h = now.replace(hour=20, minute=0, second=0, microsecond=0)
            
            # Lấy tất cả đơn hàng trong khoảng 24h
            orders = db.session.query(Order).filter(
                Order.created_at >= yesterday_20h,  # ← Từ 20:00 hôm qua
                Order.created_at < today_20h,       # ← Đến trước 20:00 hôm nay
                Order.deleted_at.is_(None)
            ).order_by(Order.created_at.desc()).all()
            
            print(f'Lấy đơn hàng từ {yesterday_20h.strftime("%d/%m/%Y %H:%M")} đến {today_20h.strftime("%d/%m/%Y %H:%M")}')
            print(f'Tìm thấy {len(orders)} đơn hàng')
            
            return [order.to_dict() for order in orders]
        
        except Exception as e:
            print(f'Lỗi lấy đơn hàng 24h: {e}')
            return []
    
    @staticmethod
    def get_all_manager_emails():
        """Lấy email của tất cả manager"""
        try:
            managers = db.session.query(User).filter(
                User.role == 'manager',
                User.deleted_at.is_(None)
            ).all()
            
            return [manager.email for manager in managers if manager.email]
            
        except Exception as e:
            print(f'Lỗi lấy email manager: {e}')
            return []
    
    @staticmethod
    def send_daily_report_to_managers():
        """
        Gửi báo cáo đơn hàng từ 20:00 hôm qua → 20:00 hôm nay
        - Gửi dù KHÔNG có đơn hàng
        """
        try:
            # LẤY ĐƠN HÀNG TRONG 24H (20:00 hôm qua → 20:00 hôm nay)
            orders_24h = OrderNotificationService.get_orders_last_24h()
            
            manager_emails = OrderNotificationService.get_all_manager_emails()
            
            if not manager_emails:
                print(' Không tìm thấy email của manager để gửi báo cáo')
                return
            
            # ✅ GỬI EMAIL DÙ KHÔNG CÓ ĐƠN HÀNG
            if not orders_24h:
                print(f'Gửi báo cáo 24h: 0 đơn hàng cho {len(manager_emails)} manager...')
            else:
                print(f'Gửi báo cáo 24h: {len(orders_24h)} đơn hàng cho {len(manager_emails)} manager...')
            
            for email in manager_emails:
                EmailService.send_daily_order_report(email, orders_24h)
        
        except Exception as e:
            print(f'Lỗi gửi báo cáo 24h: {e}')