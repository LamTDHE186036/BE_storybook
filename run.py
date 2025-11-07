# from app import create_app

# app = create_app()
# if __name__ == '__main__':
#     app.run(debug=True)

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Sử dụng biến môi trường để xác định mode
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    
    app.run(host=host, port=port, debug=debug_mode)