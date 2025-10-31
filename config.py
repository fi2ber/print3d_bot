import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
    ADMIN_CHANNEL_ID = os.getenv('ADMIN_CHANNEL_ID')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database/print3d.db')
    
    # File Storage
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'media')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # Order Statuses
    ORDER_STATUSES = {
        'new': 'Новый заказ',
        'processing': 'В обработке',
        'in_print': 'На печати',
        'in_modeling': 'На моделировании',
        'in_scanning': 'На сканировании',
        'ready_for_pickup': 'Готов к выдаче',
        'completed': 'Выполнен',
        'cancelled': 'Отменен'
    }
    
    # Service Types
    SERVICE_TYPES = {
        'print': '3D-печать',
        'modeling': '3D-моделирование',
        'scanning': '3D-сканирование'
    }
    
    # Available Materials
    MATERIALS = {
        'PLA': 'PLA (легкий в печати, биоразлагаемый)',
        'ABS': 'ABS (прочный, термостойкий)',
        'PETG': 'PETG (прозрачный, химически стойкий)',
        'TPU': 'TPU (гибкий, резиноподобный)',
        'Resin': 'Смола (высокая детализация)',
        'Nylon': 'Нейлон (высокая прочность)',
        'Metal': 'Металлический пластик',
        'Wood': 'Древесный пластик'
    }
    
    # Colors
    COLORS = [
        'Белый', 'Черный', 'Красный', 'Синий', 'Зеленый', 
        'Желтый', 'Оранжевый', 'Фиолетовый', 'Розовый', 
        'Коричневый', 'Серый', 'Прозрачный'
    ]
    
    # Strength/Accuracy Options
    STRENGTH_OPTIONS = [
        'Декоративный объект',
        'Прототип',
        'Функциональная деталь',
        'Высоконагруженная деталь'
    ]
    
    # Usage Temperatures
    TEMPERATURES = [
        'Комнатная температура',
        'До 50°C',
        'До 100°C',
        'Выше 100°C'
    ]