from flask_mail import Message
from app.extension import mail, db
import random
from datetime import datetime, timezone, timedelta
from app.models.otp import OTP
from app.models.users import User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import threading



class EmailService:
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP."""
        return str(random.randint(100000, 999999))
    
    @staticmethod
    def send_otp_email(recipient_email: str):
   
        """Tạo OTP, lưu DB và gửi email"""
        try:
            # Xóa các OTP cũ chưa sử dụng
            user_id = User.query.filter_by(email=recipient_email).first().id

            OTP.query.filter_by(user_id=user_id, is_used=False).delete()
            
            # Tạo OTP mới
            otp_code = EmailService.generate_otp()
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
            
            # Lưu vào database
            new_otp = OTP(
                user_id=user_id,
                otp_code=otp_code,
                expires_at=expires_at,
                is_used=False, 
            )
            db.session.add(new_otp)
            db.session.flush()
            
            # Tạo email với smtplib thay vì Flask-Mail
            msg = MIMEMultipart()
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = recipient_email
            msg['Subject'] = 'Password Reset OTP - StoryBook'
            
            body = f'''Hello,

You requested to reset your password. Your OTP code is:

{otp_code}

This code will expire in 10 minutes.

If you did not request this, please ignore this email.

Best regards,
StoryBook Team
'''
            msg.attach(MIMEText(body, 'plain'))
            
            # Kết nối SMTP với local_hostname hợp lệ
            server = smtplib.SMTP(
                current_app.config['MAIL_SERVER'], 
                current_app.config['MAIL_PORT'],
                local_hostname='localhost'  
            )
            server.starttls()  # Bật TLS cho port 587
            server.login(
                current_app.config['MAIL_USERNAME'], 
                current_app.config['MAIL_PASSWORD']
            )
            server.send_message(msg)
            server.quit()
            
            db.session.commit()
            
            return True, None
        
        except Exception as e:
            print("okee")
            print(f'Error sending OTP email: {e}')
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def verify_otp(email: str, otp_code: int):
        try:
            user_id = User.query.filter_by(email=email).first().id
            print(user_id, otp_code)
            otp_record = OTP.query.filter_by(
                user_id=user_id, 
                otp_code=otp_code, 
                is_used=False  
            ).first()
            
            if not otp_record:
                return False, "Invalid OTP code"
            
        
            expires_at = otp_record.expires_at
            now = datetime.now(timezone.utc)
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if expires_at < now:
                return False, "OTP has expired"
            
            # Đánh dấu OTP đã sử dụng
            otp_record.is_used = True  
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            print(e)
            return False, str(e)
        
        
    @staticmethod
    def send_order_email(customer_email: str, order_data: dict):
        
        try:
            msg = MIMEMultipart()
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = customer_email
            msg['Subject'] = f'Xác nhận giao hàng thành công - StoryBook'
            
            items_html = ""
            for item in order_data.get('items', []):
                total_item_price = item.get('price', 0) * item.get('quantity', 0)
                items_html += f"""
                    <tr>
                        <td style="padding:8px; border-bottom:1px solid #eee;">{item.get('name', 'N/A')}</td>
                        <td style="padding:8px; border-bottom:1px solid #eee; text-align:center;">{item.get('quantity', 0)}</td>
                        <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">{item.get('price', 0):,.0f}đ</td>
                        <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">{total_item_price:,.0f}đ</td>
                    </tr>
                """

            created_at = order_data.get('created_at')
            if isinstance(created_at, str):
                try:
                    from datetime import datetime
                    created_at = datetime.fromisoformat(created_at)
                except Exception:
                    pass
            formatted_date = created_at.strftime('%d/%m/%Y %H:%M') if isinstance(created_at, datetime) else created_at or 'N/A'

            body = f"""
            <html>
            <body style="font-family:Arial, sans-serif; color:#333; background-color:#f8f8f8; padding:30px;">
                <div style="max-width:600px; margin:auto; background-color:#fff; border-radius:10px; overflow:hidden; box-shadow:0 0 10px rgba(0,0,0,0.1);">
                <div style="background-color:#4CAF50; color:#fff; padding:20px; text-align:center;">
                    <h2 style="margin:0;">Xác nhận đơn hàng </h2>
                    <p style="margin:5px 0 0;">Cảm ơn bạn đã đặt hàng tại StoryBook!</p>
                </div>

                <div style="padding:20px;">
                    <h3 style="border-bottom:2px solid #eee; padding-bottom:5px;">Thông tin đơn hàng</h3>
                    <p><strong>Mã đơn hàng:</strong> {order_data.get('id')}</p>
                    <p><strong>Ngày đặt:</strong> {formatted_date}</p>
                    <p><strong>Trạng thái:</strong> {order_data.get('status', 'pending').upper()}</p>
                    <p><strong>Phương thức thanh toán:</strong> {order_data.get('payment_method', 'N/A')}</p>
                    <p><strong>Trạng thái thanh toán:</strong> {order_data.get('payment_status', 'unpaid').upper()}</p>

                    <h3 style="border-bottom:2px solid #eee; padding-bottom:5px; margin-top:25px;">Chi tiết sản phẩm</h3>
                    <table style="width:100%; border-collapse:collapse; font-size:14px;">
                        <thead style="background-color:#f2f2f2;">
                            <tr>
                                <th style="padding:8px; text-align:left;">Sản phẩm</th>
                                <th style="padding:8px;">Số lượng</th>
                                <th style="padding:8px; text-align:right;">Đơn giá</th>
                                <th style="padding:8px; text-align:right;">Thành tiền</th>
                            </tr>
                        </thead>
                        <tbody>
                            {items_html}
                        </tbody>
                    </table>

                    <div style="margin-top:20px; font-size:15px;">
                        <p><strong>Tạm tính:</strong> {order_data.get('price_before_discount', 0):,.0f}đ</p>
                        {"<p><strong>Giảm giá (" + order_data.get('discount_code') + "):</strong> -" + f"{(order_data.get('price_before_discount', 0) - order_data.get('total_price', 0)):,.0f}đ</p>" if order_data.get('discount_code') else ""}
                        <p style="font-size:18px; font-weight:bold; color:#d35400;">TỔNG CỘNG: {order_data.get('total_price', 0):,.0f}đ</p>
                    </div>

                    <p><strong>Địa chỉ giao hàng:</strong> {order_data.get('shipping_address', 'N/A')}</p>

                    <p style="margin-top:25px;">Chúng tôi sẽ liên hệ với bạn sớm nhất để xác nhận và giao hàng.</p>

                    <p style="margin:30px 0 10px 0;">Trân trọng,</p>
                    <p style="font-weight:bold; color:#2c3e50; margin:0;">StoryBook Team</p>
                    <p style="margin:4px 0 0 0; font-size:14px; color:#555;">
                        Hotline: <a href="tel:0394894565" style="color:#3498db; text-decoration:none;">0394 894 565</a><br>
                        Email: <a href="mailto:anhlam2k44@gmaill.com" style="color:#3498db; text-decoration:none;">anhlam2k44@gmaill.com</a>
                    </p>

                    <hr style="border:none; border-top:1px solid #ddd; margin:20px 0;">
                    <p style="font-size:13px; color:#999;">Email tự động, vui lòng không trả lời.</p>
                </div>
                </div>
            </body>
            </html>
            """

            msg.attach(MIMEText(body, 'html'))
                        
            # Gửi email qua SMTP
            server = smtplib.SMTP(
                current_app.config['MAIL_SERVER'], 
                current_app.config['MAIL_PORT'],
                local_hostname='localhost'
            )
            server.starttls()
            server.login(
                current_app.config['MAIL_USERNAME'], 
                current_app.config['MAIL_PASSWORD']
            )
            server.send_message(msg)
            server.quit()
            
            print(f'Đã gửi email xác nhận đơn hàng tới {customer_email}')
            return True
            
        except Exception as e:
            print(f'Lỗi gửi email đơn hàng: {e}')
            return False
        
    
    @staticmethod
    def send_order_confirmation_email(customer_email: str, order_data: dict):
        """
        Gửi email xác nhận đơn hàng ở NỀN (BACKGROUND)
        - API trả response ngay lập tức, không chờ email gửi xong
        - Email được gửi trong thread riêng
        """
        def send_in_background(app, email, data):
            with app.app_context():
                EmailService.send_order_email(email, data)
        
        # Tạo thread mới để gửi email
        thread = threading.Thread(
            target=send_in_background,
            args=(current_app._get_current_object(), customer_email, order_data)
        )
        thread.daemon = True
        thread.start()


    @staticmethod
    def send_order_shipped(customer_email: str, order_data: dict):
        
        try:
            msg = MIMEMultipart()
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = customer_email
            msg['Subject'] = f'Xác nhận đơn hàng - StoryBook'
            
            # Build items rows (HTML)
            items_rows = ""
            for item in order_data.get('items', []):
                name = item.get('name', 'N/A')
                qty = item.get('quantity', 0)
                price = item.get('price', 0) or 0
                subtotal = price * qty
                items_rows += f"""
                    <tr>
                        <td style="padding:10px 8px; border-bottom:1px solid #eee;">{name}</td>
                        <td style="padding:10px 8px; border-bottom:1px solid #eee; text-align:center;">{qty}</td>
                        <td style="padding:10px 8px; border-bottom:1px solid #eee; text-align:right;">{price:,.0f}đ</td>
                        <td style="padding:10px 8px; border-bottom:1px solid #eee; text-align:right;">{subtotal:,.0f}đ</td>
                    </tr>
                """

            discount_html = ""
            if order_data.get('discount_code'):
                discount_amount = order_data.get("price_before_discount", 0) - order_data.get("total_price", 0)
                discount_html = f"""
                    <tr>
                        <td colspan="3" style="padding:8px; text-align:right; font-size:14px; color:#2e7d32;">Mã giảm giá ({order_data.get('discount_code')}):</td>
                        <td style="padding:8px; text-align:right; font-size:14px; color:#2e7d32;">-{discount_amount:,.0f}đ</td>
                    </tr>
                """

            html_body = f"""
            <!doctype html>
            <html>
            <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>Đơn hàng #{order_data.get('id')}</title>
            </head>
            <body style="margin:0; padding:0; font-family:Arial,Helvetica,sans-serif; background:#f4f6f8;">
            <table width="100%" cellpadding="0" cellspacing="0" role="presentation">
                <tr>
                <td align="center" style="padding:20px 10px;">
                    <table width="600" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.06);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="padding:24px 32px; background:linear-gradient(90deg,#43a047,#66bb6a); color:#fff;">
                        <h1 style="margin:0; font-size:20px;">StoryBook</h1>
                        <p style="margin:6px 0 0; font-size:14px; opacity:0.95;">Thông báo: Đơn hàng đã được giao thành công </p>
                        </td>
                    </tr>

                    <!-- Order summary -->
                    <tr>
                        <td style="padding:20px 32px;">
                        <table width="100%" cellpadding="0" cellspacing="0" role="presentation">
                            <tr>
                            <td style="vertical-align:top;">
                                <p style="margin:0 0 6px; font-size:14px;"><strong>Mã đơn:</strong> {order_data.get('id')}</p>
                                <p style="margin:0 0 6px; font-size:14px;"><strong>Ngày đặt:</strong> {datetime.fromisoformat(order_data['created_at']).strftime('%d/%m/%Y %H:%M') if order_data.get('created_at') else 'N/A'}</p>
                            </td>
                            <td style="vertical-align:top; text-align:right;">
                                <p style="margin:0 0 6px; font-size:14px;"><strong>Trạng thái:</strong> <span style="color:#ff9800;">{order_data.get('status','pending').upper()}</span></p>
                                <p style="margin:0; font-size:14px;"><strong>Thanh toán:</strong> {order_data.get('payment_method','N/A')} — <em>{order_data.get('payment_status','unpaid').upper()}</em></p>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>

                    <!-- Shipping address -->
                    <tr>
                        <td style="padding:0 32px 20px 32px;">
                        <div style="background:#fafafa; padding:12px 14px; border-radius:6px; border:1px solid #f0f0f0;">
                            <strong>Địa chỉ giao hàng</strong>
                            <div style="margin-top:6px; font-size:14px; color:#555;">{order_data.get('shipping_address','N/A')}</div>
                        </div>
                        </td>
                    </tr>

                    <!-- Items table -->
                    <tr>
                        <td style="padding:0 32px 8px 32px;">
                        <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse; font-size:14px;">
                            <thead>
                            <tr style="background:#f1f8f3;">
                                <th style="text-align:left; padding:10px; font-weight:600;">Sản phẩm</th>
                                <th style="text-align:center; padding:10px; font-weight:600;">SL</th>
                                <th style="text-align:right; padding:10px; font-weight:600;">Đơn giá</th>
                                <th style="text-align:right; padding:10px; font-weight:600;">Thành tiền</th>
                            </tr>
                            </thead>
                            <tbody>
                            {items_rows}
                            </tbody>
                            <tfoot>
                            <tr>
                                <td colspan="3" style="padding:12px; text-align:right; font-size:14px;">Tạm tính:</td>
                                <td style="padding:12px; text-align:right; font-size:14px;">{order_data.get('price_before_discount',0):,.0f}đ</td>
                            </tr>
                            {discount_html}
                            <tr>
                                <td colspan="3" style="padding:12px; text-align:right; font-size:18px; font-weight:700; color:#222;">Tổng cộng:</td>
                                <td style="padding:12px; text-align:right; font-size:18px; font-weight:700; color:#2e7d32;">{order_data.get('total_price',0):,.0f}đ</td>
                            </tr>
                            </tfoot>
                        </table>
                        </td>
                    </tr>

                    <!-- CTA / Note -->
                    <tr>
                        <td style="padding:18px 32px 28px 32px;">
                        <p style="margin:0 0 10px; font-size:14px; color:#333;">
                            Đơn hàng của bạn đã giao thành công. Nếu có phản hồi hoặc yêu cầu hỗ trợ, vui lòng trả lời email này hoặc liên hệ Hotline của chúng tôi.
                        </p>
                        <p style="margin: 30px 0 10px 0;">Trân trọng,</p>
                        <p style="font-weight:bold; color:#2c3e50; margin:0;">StoryBook Team</p>
                        <p style="margin:4px 0 0 0; font-size:14px; color:#555;">
                            Hotline: <a href="tel:0394894565" style="color:#3498db; text-decoration:none;">0394 894 565</a><br>
                            Email: <a href="mailto:anhlam2k44@gmaill.com" style="color:#3498db; text-decoration:none;">anhlam2k44@gmaill.com</a>
                        </p>

                        <hr style="border:none; border-top:1px solid #ddd; margin:20px 0;">
                        <p style="font-size:13px; color:#999;">Email tự động, vui lòng không trả lời.</p>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </body>
            </html>
            """

            # Attach HTML part
            msg.attach(MIMEText(html_body, 'html'))

            
            # Gửi email qua SMTP
            server = smtplib.SMTP(
                current_app.config['MAIL_SERVER'], 
                current_app.config['MAIL_PORT'],
                local_hostname='localhost'
            )
            server.starttls()
            server.login(
                current_app.config['MAIL_USERNAME'], 
                current_app.config['MAIL_PASSWORD']
            )
            server.send_message(msg)
            server.quit()
            
            print(f'Đã gửi email xác nhận đơn hàng tới {customer_email}')
            return True
            
        except Exception as e:
            print(f'Lỗi gửi email đơn hàng: {e}')
            return False
        

    @staticmethod
    def send_order_shipped_email(customer_email: str, order_data: dict):
        """
        Gửi email xác nhận đơn hàng ở NỀN (BACKGROUND)
        - API trả response ngay lập tức, không chờ email gửi xong
        - Email được gửi trong thread riêng
        """
        def send_in_background(app, email, data):
            with app.app_context():
                EmailService.send_order_shipped(email, data)
        
        # Tạo thread mới để gửi email
        thread = threading.Thread(
            target=send_in_background,
            args=(current_app._get_current_object(), customer_email, order_data)
        )
        thread.daemon = True
        thread.start()
        
        
    @staticmethod
    def send_daily_order_report(manager_email: str, orders_data: list):
        """
        Gửi email báo cáo đơn hàng hàng ngày (20:00)
        - Gửi dù không có đơn hàng
        """
        try:
            today = datetime.now(timezone.utc).strftime("%d/%m/%Y")
            
            msg = MIMEMultipart()
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = manager_email
            msg['Subject'] = f'[StoryBook] Báo cáo đơn hàng ngày {today}'
            
            # Tính toán thống kê
            total_orders = len(orders_data)
            total_revenue = sum(order.get('total_price', 0) for order in orders_data)
            
            # Đếm theo trạng thái
            status_count = {
            'pending': 0,
            'processing': 0,
            'shipping': 0,
            'delivered': 0,
            'cancelled': 0
                            }
                    
            for order in orders_data:
                status = order.get('status', 'pending')
                if status in status_count:
                    status_count[status] += 1
            
            # Tạo bảng đơn hàng
            if orders_data:
                orders_html = ""
                for order in orders_data:
                    status_color = {
                        'pending': '#ff9800',
                        'processing': '#2196f3',
                        'shipping': '#00bcd4',
                        'delivered': '#4caf50',
                        'cancelled': '#f44336'
                    }.get(order.get('status', 'pending'), '#999')

                    created_at = order.get('created_at')
                    if created_at:
                        try:
                            created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                            created_at_str = created_dt.strftime("%d/%m/%Y %H:%M")
                        except Exception:
                            created_at_str = created_at
                    else:
                        created_at_str = "N/A"

                    orders_html += f"""
                    <tr>
                        <td style="padding:10px; border-bottom:1px solid #eee;">#{order.get('id')}</td>
                        <td style="padding:10px; border-bottom:1px solid #eee;">{order.get('customer_id')}</td>
                        <td style="padding:10px; border-bottom:1px solid #eee;">{created_at_str} (Tạo đơn)</td>
                        <td style="padding:10px; border-bottom:1px solid #eee; text-align:right; font-weight:bold;">{order.get('total_price', 0):,.0f}đ</td>
                        <td style="padding:10px; border-bottom:1px solid #eee;">
                            <span style="background-color:{status_color}; color:#fff; padding:4px 8px; border-radius:4px; font-size:12px;">
                                {order.get('status', 'pending').upper()}
                            </span>
                        </td>
                        <td style="padding:10px; border-bottom:1px solid #eee;">{order.get('payment_method', 'N/A')}</td>
                    </tr>
                    """

                orders_table = f"""
                <div style="padding:20px 30px;">
                    <h3 style="margin:0 0 15px; color:#333; font-size:18px;">Chi tiết đơn hàng</h3>
                    <table style="width:100%; border-collapse:collapse; font-size:14px;">
                        <thead>
                            <tr style="background-color:#667eea; color:#fff;">
                                <th style="padding:12px 10px; text-align:left;">Mã ĐH</th>
                                <th style="padding:12px 10px; text-align:left;">KH ID</th>
                                <th style="padding:12px 10px; text-align:left;">Thời gian tạo</th>
                                <th style="padding:12px 10px; text-align:right;">Tổng tiền</th>
                                <th style="padding:12px 10px; text-align:left;">Trạng thái</th>
                                <th style="padding:12px 10px; text-align:left;">Thanh toán</th>
                            </tr>
                        </thead>
                        <tbody>
                            {orders_html}
                        </tbody>
                    </table>
                </div>
                """
            else:
                orders_table = """
                <div style="padding:20px 30px; text-align:center;">
                    <p style="font-size:16px; color:#999; padding:40px 0;">
                        Không có đơn hàng nào trong ngày hôm nay
                    </p>
                </div>
                """

            
            body = f"""
                    <html>
                    <body style="font-family:Arial, sans-serif; color:#333; background-color:#f5f5f5; padding:20px;">
                        <div style="max-width:900px; margin:auto; background-color:#fff; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                            
                            <!-- Header -->
                            <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:#fff; padding:20px 30px;">
                                <h2 style="margin:0; font-size:24px;">📊 Báo cáo đơn hàng ngày</h2>
                                <p style="margin:8px 0 0; font-size:14px; opacity:0.9;">
                                    Ngày: {today} | Thời gian gửi: 20:00 UTC
                                </p>
                            </div>
                            
                            <!-- Summary Stats -->
                            <div style="padding:20px 30px; background-color:#f9f9f9; border-bottom:2px solid #eee;">
                                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:15px;">
                                    <div style="text-align:center; padding:15px; background:#fff; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
                                        <p style="margin:0; font-size:28px; font-weight:bold; color:#667eea;">{total_orders}</p>
                                        <p style="margin:4px 0 0; font-size:13px; color:#666;">Tổng đơn hàng</p>
                                    </div>
                                    <div style="text-align:center; padding:15px; background:#fff; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
                                        <p style="margin:0; font-size:28px; font-weight:bold; color:#4caf50;">{total_revenue:,.0f}đ</p>
                                        <p style="margin:4px 0 0; font-size:13px; color:#666;">Doanh thu</p>
                                    </div>
                                    <div style="text-align:center; padding:15px; background:#fff; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
                                        <p style="margin:0; font-size:28px; font-weight:bold; color:#2196f3;">{status_count['delivered']}</p>
                                        <p style="margin:4px 0 0; font-size:13px; color:#666;">Đã giao</p>
                                    </div>
                                </div>
                                
                                <div style="margin-top:15px; padding:15px; background:#fff; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
                                    <p style="margin:0; font-size:13px; color:#666;">
                                        <span style="color:#ff9800;">⏳ Chờ xử lý: {status_count['pending']}</span> | 
                                        <span style="color:#2196f3;">🔄 Đang xử lý: {status_count['processing']}</span> | 
                                        <span style="color:#00bcd4;">🚚 Đang giao: {status_count['shipping']}</span> | 
                                        <span style="color:#4caf50;">✅ Đã giao: {status_count['delivered']}</span> | 
                                        <span style="color:#f44336;">❌ Đã hủy: {status_count['cancelled']}</span>
                                    </p>
                                </div>
                            </div>
                            
                            <!-- Orders Table -->
                            {orders_table}
                            
                            <!-- Footer -->
                            <div style="padding:20px 30px; background-color:#f9f9f9; border-top:2px solid #eee;">
                                <p style="margin:0; font-size:13px; color:#666;">
                                    Email tự động từ hệ thống <strong>StoryBook</strong><br>
                                    Báo cáo được gửi vào 20:00 UTC hàng ngày<br>
                                    Ngày gửi: {datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S")} UTC
                                </p>
                            </div>
                            
                        </div>
                    </body>
                    </html>
                    """

            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(
                current_app.config['MAIL_SERVER'], 
                current_app.config['MAIL_PORT'],
                local_hostname='localhost'
            )
            server.starttls()
            server.login(
                current_app.config['MAIL_USERNAME'], 
                current_app.config['MAIL_PASSWORD']
            )
            server.send_message(msg)
            server.quit()
            
            print(f'Đã gửi báo cáo hàng ngày ({total_orders} đơn hàng) tới {manager_email}')
            return True
        
        except Exception as e:
            print(f' Lỗi gửi báo cáo hàng ngày: {e}')
            return False    
        
    
        
        
        