# Развертывание Print3DUz Bot на DigitalOcean

## 🌊 Подготовка сервера DigitalOcean

### 1. Создание Droplet
1. Зарегистрируйтесь на [DigitalOcean](https://www.digitalocean.com)
2. Создайте новый Droplet:
   - **Операционная система**: Ubuntu 22.04 LTS
   - **План**: Basic
   - **CPU**: 1 vCPU
   - **RAM**: 1 GB
   - **SSD**: 25 GB
   - **Цена**: $6/месяц

### 2. Настройка доступа
```bash
# Подключение к серверу
ssh root@your_server_ip

# Обновление системы
apt update && apt upgrade -y

# Установка необходимых пакетов
apt install python3-pip python3-venv git nginx supervisor -y
```

## 🐍 Установка Python и зависимостей

### 1. Установка Python
```bash
# Проверка версии Python
python3 --version

# Установка virtual environment
apt install python3-venv -y

# Создание виртуального окружения
mkdir -p /opt/print3d_bot
cd /opt/print3d_bot
python3 -m venv venv
source venv/bin/activate
```

### 2. Установка проекта
```bash
# Клонирование репозитория (или загрузка файлов)
git clone https://github.com/yourusername/print3d_bot.git .

# Установка зависимостей
pip install -r requirements.txt

# Создание директорий
mkdir -p logs media/files media/photos database

# Настройка прав
chmod +x run_bot.py run_admin.py deploy.sh
chmod -R 755 media/
chmod -R 755 database/
```

## 🔧 Настройка конфигурации

### 1. Создание .env файла
```bash
cp .env.example .env
nano .env
```

### 2. Заполнение конфигурации
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
ADMIN_CHAT_ID=your_admin_chat_id_here
ADMIN_CHANNEL_ID=your_channel_id_here

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here_change_in_production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# Database Configuration
DATABASE_URL=sqlite:///database/print3d.db

# File Storage
UPLOAD_FOLDER=media
MAX_CONTENT_LENGTH=16777216
```

## 🚀 Настройка systemd сервисов

### 1. Создание сервиса для бота
```bash
sudo tee /etc/systemd/system/print3d-bot.service > /dev/null <<EOF
[Unit]
Description=Print3DUz Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/print3d_bot
ExecStart=/opt/print3d_bot/venv/bin/python3 /opt/print3d_bot/run_bot.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/print3d_bot

[Install]
WantedBy=multi-user.target
EOF
```

### 2. Создание сервиса для админ-панели
```bash
sudo tee /etc/systemd/system/print3d-admin.service > /dev/null <<EOF
[Unit]
Description=Print3DUz Admin Panel
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/print3d_bot
ExecStart=/opt/print3d_bot/venv/bin/python3 /opt/print3d_admin/run_admin.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/print3d_bot
Environment=FLASK_ENV=production

[Install]
WantedBy=multi-user.target
EOF
```

### 3. Активация сервисов
```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Запуск сервисов
sudo systemctl start print3d-bot
sudo systemctl start print3d-admin

# Добавление в автозагрузку
sudo systemctl enable print3d-bot
sudo systemctl enable print3d-admin

# Проверка статуса
sudo systemctl status print3d-bot
sudo systemctl status print3d-admin
```

## 🌐 Настройка Nginx (опционально)

### 1. Установка Nginx
```bash
apt install nginx -y
```

### 2. Настройка конфигурации
```bash
sudo tee /etc/nginx/sites-available/print3d_bot > /dev/null <<EOF
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /opt/print3d_bot/static;
        expires 30d;
    }

    location /media {
        alias /opt/print3d_bot/media;
        expires 30d;
    }
}
EOF
```

### 3. Активация сайта
```bash
sudo ln -s /etc/nginx/sites-available/print3d_bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 Настройка firewall

### 1. Установка UFW
```bash
apt install ufw -y

# Базовые правила
ufw default deny incoming
ufw default allow outgoing

# Разрешение SSH
ufw allow ssh

# Разрешение HTTP/HTTPS (если используется Nginx)
ufw allow 'Nginx Full'

# Активация firewall
ufw enable
```

### 2. Проверка статуса
```bash
ufw status
```

## 📊 Мониторинг и логи

### 1. Просмотр логов systemd
```bash
# Логи бота
sudo journalctl -u print3d-bot -f

# Логи админ-панели
sudo journalctl -u print3d-admin -f

# Все логи
sudo journalctl -f
```

### 2. Создание файлов логов
```bash
# Создание лог-файлов
touch /opt/print3d_bot/logs/bot.log
touch /opt/print3d_bot/logs/admin.log

# Настройка ротации логов
sudo tee /etc/logrotate.d/print3d_bot > /dev/null <<EOF
/opt/print3d_bot/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    notifempty
    create 0644 root root
}
EOF
```

## 🔄 Обновление приложения

### 1. Остановка сервисов
```bash
sudo systemctl stop print3d-bot
sudo systemctl stop print3d-admin
```

### 2. Обновление кода
```bash
cd /opt/print3d_bot
# git pull origin main  # если используется git
# или замените файлы вручную
```

### 3. Перезапуск сервисов
```bash
sudo systemctl start print3d-bot
sudo systemctl start print3d-admin
```

## 🗄 Резервное копирование

### 1. Скрипт резервного копирования
```bash
sudo tee /opt/print3d_bot/backup.sh > /dev/null <<EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/print3d_bot"

mkdir -p \$BACKUP_DIR

# Копирование базы данных
cp /opt/print3d_bot/database/print3d.db \$BACKUP_DIR/print3d_\$DATE.db

# Копирование загруженных файлов
tar -czf \$BACKUP_DIR/media_\$DATE.tar.gz -C /opt/print3d_bot media/

# Копирование конфигурации
cp /opt/print3d_bot/.env \$BACKUP_DIR/env_\$DATE

# Удаление старых бэкапов (старше 30 дней)
find \$BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: \$DATE"
EOF

chmod +x /opt/print3d_bot/backup.sh
```

### 2. Настройка cron
```bash
# Ежедневное резервное копирование в 2:00 AM
sudo crontab -e
# Добавить строку:
0 2 * * * /opt/print3d_bot/backup.sh >> /var/log/print3d_backup.log 2>&1
```

## 📈 Мониторинг

### 1. Установка мониторинга (опционально)
```bash
# Установка htop для мониторинга ресурсов
apt install htop -y

# Установка netdata для детального мониторинга
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

### 2. Настройка алертов
```bash
# Проверка работы сервисов каждые 5 минут
sudo crontab -e
# Добавить строки:
*/5 * * * * systemctl is-active --quiet print3d-bot || systemctl restart print3d-bot
*/5 * * * * systemctl is-active --quiet print3d-admin || systemctl restart print3d-admin
```

## 🔧 Управление сервисами

### Основные команды:
```bash
# Запуск
sudo systemctl start print3d-bot
sudo systemctl start print3d-admin

# Остановка
sudo systemctl stop print3d-bot
sudo systemctl stop print3d-admin

# Перезапуск
sudo systemctl restart print3d-bot
sudo systemctl restart print3d-admin

# Проверка статуса
sudo systemctl status print3d-bot
sudo systemctl status print3d-admin

# Просмотр логов
sudo journalctl -u print3d-bot -f
sudo journalctl -u print3d-admin -f

# Добавление/удаление из автозагрузки
sudo systemctl enable print3d-bot
sudo systemctl disable print3d-bot
```

## 📋 Чек-лист запуска

### Перед запуском:
- [ ] Сервер создан и настроен
- [ ] Python и зависимости установлены
- [ ] .env файл заполнен
- [ ] Права на файлы настроены
- [ ] Firewall настроен
- [ ] Nginx настроен (если используется)
- [ ] Сервисы созданы

### После запуска:
- [ ] Бот отвечает на команды
- [ ] Админ-панель доступна
- [ ] Загрузка файлов работает
- [ ] Уведомления приходят
- [ ] Резервное копирование настроено
- [ ] Мониторинг работает

## 🆘 Решение проблем

### Бот не запускается:
1. Проверьте логи: `sudo journalctl -u print3d-bot -f`
2. Проверьте токен в .env файле
3. Убедитесь, что права на файлы корректны

### Админ-панель не доступна:
1. Проверьте логи: `sudo journalctl -u print3d-admin -f`
2. Проверьте firewall
3. Проверьте Nginx (если используется)

### Ошибки с базой данных:
1. Проверьте права на директорию database/
2. Убедитесь, что есть свободное место на диске
3. Проверьте логи на наличие ошибок SQLite

## 📞 Поддержка

Если возникли проблемы при развертывании:
- Проверьте логи сервисов
- Убедитесь, что все зависимости установлены
- Проверьте конфигурационные файлы
- Обратитесь за помощью к разработчику

## 🎉 Поздравляем!

Ваш Print3DUz Bot успешно развернут на DigitalOcean!

- Telegram-бот: запущен и готов принимать заказы
- Админ-панель: доступна по адресу вашего сервера
- Мониторинг: настроен и работает
- Резервное копирование: автоматическое

Теперь вы можете начать принимать заказы на 3D-печать в Самарканде!