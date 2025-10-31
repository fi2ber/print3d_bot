class Localization:
    MESSAGES = {
        'ru': {
            'welcome': 'Добро пожаловать в Print3DUz! 🖨️\n\nМы предоставляем профессиональные услуги 3D-печати, моделирования и сканирования в Самарканде.\n\nВыберите язык:',
            'main_menu': '🏠 Главное меню',
            'make_order': '📦 Сделать заказ',
            'about_us': 'ℹ️ О нас',
            'my_orders': '🧾 Мои заказы',
            'contact': '📞 Связаться',
            'select_service': 'Отлично! Какой тип услуги вас интересует?',
            'service_print': '🖨️ 3D-печать (у меня есть модель)',
            'service_modeling': '🎨 3D-моделирование (по фото/описанию)',
            'service_scanning': '📷 3D-сканирование (нужен 3D-файл)',
            'send_stl_file': 'Пожалуйста, отправьте ваш STL-файл для печати:',
            'select_material': 'Выберите материал для печати:',
            'select_color': 'Выберите цвет изделия:',
            'select_strength': 'Укажите назначение изделия:',
            'select_temperature': 'При каких температурах будет использоваться изделие?',
            'enter_quantity': 'Сколько копий нужно напечатать?',
            'enter_deadline': 'Есть ли ограничения по срокам? (если нет - напишите "нет")',
            'enter_name': 'Введите ваше имя:',
            'share_phone': 'Поделитесь номером телефона',
            'enter_location': 'Укажите вашу локацию (для доставки/забора):',
            'order_received': '✅ Ваш заказ принят!\n\nНомер заказа: #{order_id}\nМы свяжемся с вами в ближайшее время для уточнения деталей.',
            'about_text': '🏭 **О Print3DUz**\n\nМы предоставляем профессиональные услуги:\n\n🖨️ **3D-печать**\n📐 **3D-моделирование**\n📷 **3D-сканирование**\n\n**Материалы:** PLA, ABS, PETG, Resin, TPU и другие\n\n**Максимальные размеры печати:** 300x300x400 мм\n\n**Сроки:** от 1 до 7 дней\n\n**Преимущества:**\n✅ Высокое качество\n✅ Индивидуальный подход\n✅ Опытные специалисты\n✅ Современное оборудование',
            'contact_info': '📞 **Контакты**\n\n📱 Телефон: +998 (90) 123-45-67\n📧 Email: info@print3duz.uz\n📍 Адрес: г. Самарканд, ул. Мирзаева, 15\n\n🌐 Telegram: @Print3DUz\n📸 Instagram: @print3duz',
            'my_orders_empty': 'У вас пока нет заказов.',
            'order_status_changed': 'Ваш заказ #{order_id} изменил статус на: {status}',
            'send_photo_desc': 'Отправьте фото, эскиз или подробное описание:',
            'describe_object': 'Опишите объект для сканирования (размер, материал, цель):',
            'cancel': '❌ Отмена',
            'back': '⬅️ Назад',
            'confirm': '✅ Подтвердить'
        },
        'uz': {
            'welcome': 'Print3DUz ga xush kelibsiz! 🖨️\n\nBiz Samarqandda professional 3D-bosib berish, modellashtirish va skanerlash xizmatlarini taqdim etamiz.\n\nTilni tanlang:',
            'main_menu': '🏠 Bosh menyu',
            'make_order': '📦 Buyurtma berish',
            'about_us': 'ℹ️ Biz haqimizda',
            'my_orders': '🧾 Mening buyurtmalarim',
            'contact': '📞 Bog‘lanish',
            'select_service': 'Ajoyib! Qanday turdagi xizmatga qiziqasiz?',
            'service_print': '🖨️ 3D-bosib berish (menda model bor)',
            'service_modeling': '🎨 3D-modellashtirish (foto/tavsif asosida)',
            'service_scanning': '📷 3D-skanerlash (3D-fayl kerak)',
            'send_stl_file': 'Iltimos, bosib berish uchun STL-faylingizni yuboring:',
            'select_material': 'Bosib berish uchun materialni tanlang:',
            'select_color': 'Narsaning rangini tanlang:',
            'select_strength': 'Narsaning maqsadini ko‘rsating:',
            'select_temperature': 'Narsa qanday haroratda ishlatiladi?',
            'enter_quantity': 'Necha nusxa bosib berish kerak?',
            'enter_deadline': 'Muddat cheklovi bormi? (yo‘q bo‘lsa "yo‘q" deb yozing)',
            'enter_name': 'Ismingizni kiriting:',
            'share_phone': 'Telefon raqamingizni baham ko‘ring',
            'enter_location': 'Joylashuvingizni ko‘rsating (yetkazib berish/olish uchun):',
            'order_received': '✅ Buyurtmangiz qabul qilindi!\n\nBuyurtma raqami: #{order_id}\nTez orada siz bilan bog‘lanamiz.',
            'about_text': '🏭 **Print3DUz haqida**\n\nBiz professional xizmatlar taqdim etamiz:\n\n🖨️ **3D-bosib berish**\n📐 **3D-modellashtirish**\n📷 **3D-skanerlash**\n\n**Materiallar:** PLA, ABS, PETG, Resin, TPU va boshqalar\n\n**Maksimal o‘lchamlar:** 300x300x400 mm\n\n**Muddati:** 1 dan 7 kunga\n\n**Afzalliklari:**\n✅ Yuqori sifat\n✅ Individual yondashuv\n✅ Tajriba ega mutaxassislar\n✅ Zamonaviy jihozlar',
            'contact_info': '📞 **Kontaktlar**\n\n📱 Telefon: +998 (90) 123-45-67\n📧 Email: info@print3duz.uz\n📍 Manzil: Samarqand sh., Mirzaeva ko‘chasi, 15\n\n🌐 Telegram: @Print3DUz\n📸 Instagram: @print3duz',
            'my_orders_empty': 'Sizda hali buyurtmalar yo‘q.',
            'order_status_changed': 'Buyurtmangiz #{order_id} holati o‘zgarib: {status} bo‘ldi',
            'send_photo_desc': 'Foto, eskiz yoki batafsil tavsif yuboring:',
            'describe_object': 'Skanerlanadigan obyektni tavsiflang (o‘lcham, material, maqsad):',
            'cancel': '❌ Bekor qilish',
            'back': '⬅️ Orqaga',
            'confirm': '✅ Tasdiqlash'
        }
    }
    
    @classmethod
    def get_text(cls, language, key, **kwargs):
        text = cls.MESSAGES.get(language, cls.MESSAGES['ru']).get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text
    
    @classmethod
    def get_status_text(cls, language, status):
        status_mapping = {
            'ru': {
                'new': 'Новый заказ',
                'processing': 'В обработке',
                'in_print': 'На печати',
                'in_modeling': 'На моделировании',
                'in_scanning': 'На сканировании',
                'ready_for_pickup': 'Готов к выдаче',
                'completed': 'Выполнен',
                'cancelled': 'Отменен'
            },
            'uz': {
                'new': 'Yangi buyurtma',
                'processing': 'Jarayonda',
                'in_print': 'Bosib berilmoqda',
                'in_modeling': 'Modellashtirilmoqda',
                'in_scanning': 'Skanerlanmoqda',
                'ready_for_pickup': 'Olishga tayyor',
                'completed': 'Bajarildi',
                'cancelled': 'Bekor qilindi'
            }
        }
        return status_mapping.get(language, status_mapping['ru']).get(status, status)
