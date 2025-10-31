#!/bin/bash

# Скрипт для развертывания Print3DUz Bot на сервере DigitalOcean

echo "🚀 Начало развертывания Print3DUz Bot..."

# Проверка наличия необходимых инструментов
command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 не установлен"; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "❌ pip3 не установлен"; exit 1; }

# Создание директорий
mkdir -p logs
mkdir -p media/files
mkdir -p media/photos
mkdir -p database

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

# Создание systemd сервисов
echo "🔧 Настройка сервисов..."

# Telegram Bot Service
sudo tee /etc/systemd/system/print3d-bot.service > /dev/null <<EOF
[Unit]
Description=Print3DUz Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/run_bot.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=$(pwd)

[Install]
WantedBy=multi-user.target
EOF

# Flask Admin Service
sudo tee /etc/systemd/system/print3d-admin.service > /dev/null <<EOF
[Unit]
Description=Print3DUz Admin Panel
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/run_admin.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=$(pwd)
Environment=FLASK_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# Перезагрузка systemd
sudo systemctl daemon-reload

# Настройка прав на файлы
chmod +x run_bot.py
chmod +x run_admin.py
chmod -R 755 media/
chmod -R 755 database/

echo "✅ Развертывание завершено!"
echo ""
echo "📋 Дальнейшие шаги:"
echo "1. Отредактируйте файл .env с вашими данными"
echo "2. Запустите сервисы:"
echo "   sudo systemctl start print3d-bot"
echo "   sudo systemctl start print3d-admin"
echo "3. Добавьте в автозагрузку:"
echo "   sudo systemctl enable print3d-bot"
echo "   sudo systemctl enable print3d-admin"
echo ""
echo "📊 Управление сервисами:"
echo "- Проверка статуса: sudo systemctl status print3d-bot"
echo "- Просмотр логов: sudo journalctl -u print3d-bot -f"
echo "- Перезапуск: sudo systemctl restart print3d-bot"
echo ""
echo "🌐 Админ-панель будет доступна по адресу сервера на порту 5000"