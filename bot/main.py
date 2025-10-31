import asyncio
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes, ConversationHandler
from telegram.constants import ParseMode

from config import Config
from database.models import Database
from utils.localization import Localization

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = Database(Config.DATABASE_URL)

# Conversation states
LANGUAGE, MAIN_MENU, SERVICE_TYPE, PRINT_FILE, PRINT_DETAILS, MODELING_DESC, SCANNING_DESC, CONTACT_INFO = range(8)

# Define keyboards
def get_language_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
        [InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='lang_uz')]
    ])

def get_main_menu_keyboard(lang):
    return ReplyKeyboardMarkup([
        [Localization.get_text(lang, 'make_order')],
        [Localization.get_text(lang, 'about_us')],
        [Localization.get_text(lang, 'my_orders')],
        [Localization.get_text(lang, 'contact')]
    ], resize_keyboard=True)

def get_service_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(Localization.get_text(lang, 'service_print'), callback_data='service_print')],
        [InlineKeyboardButton(Localization.get_text(lang, 'service_modeling'), callback_data='service_modeling')],
        [InlineKeyboardButton(Localization.get_text(lang, 'service_scanning'), callback_data='service_scanning')]
    ])

def get_material_keyboard(lang):
    materials = list(Config.MATERIALS.keys())
    keyboard = []
    for i in range(0, len(materials), 2):
        row = []
        row.append(InlineKeyboardButton(materials[i], callback_data=f'material_{materials[i]}'))
        if i + 1 < len(materials):
            row.append(InlineKeyboardButton(materials[i + 1], callback_data=f'material_{materials[i + 1]}'))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def get_color_keyboard(lang):
    colors = Config.COLORS
    keyboard = []
    for i in range(0, len(colors), 3):
        row = []
        row.append(InlineKeyboardButton(colors[i], callback_data=f'color_{colors[i]}'))
        if i + 1 < len(colors):
            row.append(InlineKeyboardButton(colors[i + 1], callback_data=f'color_{colors[i + 1]}'))
        if i + 2 < len(colors):
            row.append(InlineKeyboardButton(colors[i + 2], callback_data=f'color_{colors[i + 2]}'))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def get_strength_keyboard(lang):
    strengths = Config.STRENGTH_OPTIONS
    keyboard = []
    for strength in strengths:
        keyboard.append([InlineKeyboardButton(strength, callback_data=f'strength_{strength}')])
    return InlineKeyboardMarkup(keyboard)

def get_temperature_keyboard(lang):
    temps = Config.TEMPERATURES
    keyboard = []
    for temp in temps:
        keyboard.append([InlineKeyboardButton(temp, callback_data=f'temp_{temp}')])
    return InlineKeyboardMarkup(keyboard)

def get_phone_keyboard(lang):
    return ReplyKeyboardMarkup([
        [KeyboardButton(Localization.get_text(lang, 'share_phone'), request_contact=True)],
        [Localization.get_text(lang, 'cancel')]
    ], resize_keyboard=True)

# Helper functions
async def save_file(file, file_type):
    """Save uploaded file and return path"""
    try:
        upload_dir = Path(Config.UPLOAD_FOLDER)
        if file_type == 'stl':
            upload_dir = upload_dir / 'files'
        else:
            upload_dir = upload_dir / 'photos'
        
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / file.file_name
        await file.download_to_drive(file_path)
        return str(file_path)
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return None

async def notify_admin(order):
    """Send notification to admin about new order"""
    try:
        message = f"🆕 Новый заказ #{order.id}\n\n"
        message += f"Услуга: {Config.SERVICE_TYPES.get(order.service_type, order.service_type)}\n"
        message += f"Клиент: {order.name}\n"
        message += f"Телефон: {order.phone}\n"
        message += f"Язык: {'Русский' if order.language == 'ru' else 'Узбекский'}\n"
        if order.description:
            message += f"Описание: {order.description[:100]}...\n"
        message += f"Статус: {Config.ORDER_STATUSES.get(order.status, order.status)}\n"
        message += f"Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}"
        
        # Send to admin channel/personal chat
        if Config.ADMIN_CHANNEL_ID:
            await bot.send_message(Config.ADMIN_CHANNEL_ID, message)
        elif Config.ADMIN_CHAT_ID:
            await bot.send_message(Config.ADMIN_CHAT_ID, message)
            
    except Exception as e:
        logger.error(f"Error notifying admin: {e}")

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    
    # Save or update user
    db_user = db.get_user(user.id)
    if not db_user:
        db.add_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
    
    await update.message.reply_text(
        Localization.get_text('ru', 'welcome'),
        reply_markup=get_language_keyboard()
    )
    return LANGUAGE

async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection"""
    query = update.callback_query
    await query.answer()
    
    lang = query.data.split('_')[1]
    
    # Update user language
    db.update_user_language(query.from_user.id, lang)
    
    context.user_data['language'] = lang
    
    await query.edit_message_text(
        Localization.get_text(lang, 'welcome'),
        reply_markup=get_main_menu_keyboard(lang)
    )
    return MAIN_MENU

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle main menu selections"""
    text = update.message.text
    user = update.effective_user
    
    # Get user language
    db_user = db.get_user(user.id)
    lang = db_user.language if db_user else 'ru'
    context.user_data['language'] = lang
    
    if text == Localization.get_text(lang, 'make_order'):
        await update.message.reply_text(
            Localization.get_text(lang, 'select_service'),
            reply_markup=get_service_keyboard(lang)
        )
        return SERVICE_TYPE
    
    elif text == Localization.get_text(lang, 'about_us'):
        await update.message.reply_text(
            Localization.get_text(lang, 'about_text'),
            parse_mode=ParseMode.MARKDOWN
        )
        return MAIN_MENU
    
    elif text == Localization.get_text(lang, 'my_orders'):
        orders = db.get_user_orders(user.id)
        if not orders:
            await update.message.reply_text(Localization.get_text(lang, 'my_orders_empty'))
        else:
            orders_text = f"📋 {Localization.get_text(lang, 'my_orders')}\n\n"
            for order in orders[:5]:  # Show last 5 orders
                status_text = Localization.get_status_text(lang, order.status)
                orders_text += f"Заказ #{order.id} - {status_text}\n"
                orders_text += f"Услуга: {Config.SERVICE_TYPES.get(order.service_type, order.service_type)}\n"
                orders_text += f"Дата: {order.created_at.strftime('%d.%m.%Y')}\n\n"
            
            await update.message.reply_text(orders_text)
        return MAIN_MENU
    
    elif text == Localization.get_text(lang, 'contact'):
        await update.message.reply_text(
            Localization.get_text(lang, 'contact_info'),
            parse_mode=ParseMode.MARKDOWN
        )
        return MAIN_MENU
    
    return MAIN_MENU

async def service_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle service type selection"""
    query = update.callback_query
    await query.answer()
    
    service = query.data.split('_')[1]
    lang = context.user_data.get('language', 'ru')
    
    context.user_data['service_type'] = service
    
    if service == 'print':
        await query.edit_message_text(Localization.get_text(lang, 'send_stl_file'))
        return PRINT_FILE
    
    elif service == 'modeling':
        await query.edit_message_text(Localization.get_text(lang, 'send_photo_desc'))
        return MODELING_DESC
    
    elif service == 'scanning':
        await query.edit_message_text(Localization.get_text(lang, 'describe_object'))
        return SCANNING_DESC
    
    return SERVICE_TYPE

async def handle_print_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle STL file upload for printing"""
    document = update.message.document
    lang = context.user_data.get('language', 'ru')
    
    if not document.file_name.lower().endswith('.stl'):
        await update.message.reply_text("Пожалуйста, отправьте файл в формате STL.")
        return PRINT_FILE
    
    # Save file
    file_path = await save_file(document, 'stl')
    if not file_path:
        await update.message.reply_text("Ошибка при сохранении файла. Попробуйте еще раз.")
        return PRINT_FILE
    
    context.user_data['file_path'] = file_path
    context.user_data['file_name'] = document.file_name
    
    await update.message.reply_text(
        Localization.get_text(lang, 'select_material'),
        reply_markup=get_material_keyboard(lang)
    )
    return PRINT_DETAILS

async def handle_material_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle material selection"""
    query = update.callback_query
    await query.answer()
    
    material = query.data.split('_')[1]
    lang = context.user_data.get('language', 'ru')
    
    context.user_data['material'] = material
    
    await query.edit_message_text(
        Localization.get_text(lang, 'select_color'),
        reply_markup=get_color_keyboard(lang)
    )
    return PRINT_DETAILS

async def handle_color_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle color selection"""
    query = update.callback_query
    await query.answer()
    
    color = query.data.split('_')[1]
    lang = context.user_data.get('language', 'ru')
    
    context.user_data['color'] = color
    
    await query.edit_message_text(
        Localization.get_text(lang, 'select_strength'),
        reply_markup=get_strength_keyboard(lang)
    )
    return PRINT_DETAILS

async def handle_strength_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle strength/accuracy selection"""
    query = update.callback_query
    await query.answer()
    
    strength = query.data.split('_', 1)[1]  # Split only on first underscore
    lang = context.user_data.get('language', 'ru')
    
    context.user_data['strength_accuracy'] = strength
    
    await query.edit_message_text(
        Localization.get_text(lang, 'select_temperature'),
        reply_markup=get_temperature_keyboard(lang)
    )
    return PRINT_DETAILS

async def handle_temperature_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle temperature selection"""
    query = update.callback_query
    await query.answer()
    
    temp = query.data.split('_', 1)[1]  # Split only on first underscore
    lang = context.user_data.get('language', 'ru')
    
    context.user_data['usage_temp'] = temp
    
    await query.edit_message_text(Localization.get_text(lang, 'enter_quantity'))
    return PRINT_DETAILS

async def handle_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quantity input"""
    try:
        quantity = int(update.message.text)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректное количество.")
        return PRINT_DETAILS
    
    context.user_data['quantity'] = quantity
    lang = context.user_data.get('language', 'ru')
    
    await update.message.reply_text(Localization.get_text(lang, 'enter_deadline'))
    return PRINT_DETAILS

async def handle_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle deadline input"""
    deadline = update.message.text
    lang = context.user_data.get('language', 'ru')
    
    context.user_data['deadline'] = deadline if deadline.lower() != 'нет' else None
    
    await update.message.reply_text(Localization.get_text(lang, 'enter_name'))
    return CONTACT_INFO

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle name input"""
    name = update.message.text
    lang = context.user_data.get('language', 'ru')
    
    context.user_data['name'] = name
    
    await update.message.reply_text(
        Localization.get_text(lang, 'share_phone'),
        reply_markup=get_phone_keyboard(lang)
    )
    return CONTACT_INFO

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle phone number input"""
    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        phone = update.message.text
    
    lang = context.user_data.get('language', 'ru')
    context.user_data['phone'] = phone
    
    await update.message.reply_text(
        Localization.get_text(lang, 'enter_location'),
        reply_markup=ReplyKeyboardMarkup([[Localization.get_text(lang, 'cancel')]], resize_keyboard=True)
    )
    return CONTACT_INFO

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle location input and create order"""
    location = update.message.text
    user = update.effective_user
    lang = context.user_data.get('language', 'ru')
    
    if location == Localization.get_text(lang, 'cancel'):
        await update.message.reply_text(
            Localization.get_text(lang, 'main_menu'),
            reply_markup=get_main_menu_keyboard(lang)
        )
        return MAIN_MENU
    
    context.user_data['location'] = location
    
    # Create order
    try:
        order_data = {
            'user_id': str(user.id),
            'username': user.username,
            'name': context.user_data['name'],
            'phone': context.user_data['phone'],
            'service_type': context.user_data['service_type'],
            'file_path': context.user_data.get('file_path'),
            'material': context.user_data.get('material'),
            'color': context.user_data.get('color'),
            'strength_accuracy': context.user_data.get('strength_accuracy'),
            'usage_temp': context.user_data.get('usage_temp'),
            'quantity': context.user_data.get('quantity', 1),
            'deadline': context.user_data.get('deadline'),
            'location': location,
            'language': lang,
            'description': f"Файл: {context.user_data.get('file_name', 'Без файла')}"
        }
        
        order = db.add_order(**order_data)
        
        # Notify admin
        await notify_admin(order)
        
        # Clear user data
        context.user_data.clear()
        
        await update.message.reply_text(
            Localization.get_text(lang, 'order_received', order_id=order.id),
            reply_markup=get_main_menu_keyboard(lang)
        )
        
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        await update.message.reply_text(
            "Произошла ошибка при создании заказа. Попробуйте позже.",
            reply_markup=get_main_menu_keyboard(lang)
        )
    
    return MAIN_MENU

async def handle_modeling_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle modeling description/photo"""
    lang = context.user_data.get('language', 'ru')
    
    if update.message.photo:
        # Save photo
        photo = update.message.photo[-1]  # Get highest quality photo
        file_path = await save_file(await photo.get_file(), 'photo')
        if file_path:
            context.user_data['file_path'] = file_path
        description = "Фото приложено"
    elif update.message.document:
        # Save document
        file_path = await save_file(await update.message.document.get_file(), 'file')
        if file_path:
            context.user_data['file_path'] = file_path
        description = f"Файл: {update.message.document.file_name}"
    else:
        description = update.message.text
    
    context.user_data['description'] = description
    
    await update.message.reply_text(Localization.get_text(lang, 'enter_name'))
    return CONTACT_INFO

async def handle_scanning_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle scanning description"""
    description = update.message.text
    lang = context.user_data.get('language', 'ru')
    
    context.user_data['description'] = description
    
    await update.message.reply_text(Localization.get_text(lang, 'enter_name'))
    return CONTACT_INFO

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current operation"""
    user = update.effective_user
    db_user = db.get_user(user.id)
    lang = db_user.language if db_user else 'ru'
    
    context.user_data.clear()
    
    await update.message.reply_text(
        Localization.get_text(lang, 'main_menu'),
        reply_markup=get_main_menu_keyboard(lang)
    )
    return MAIN_MENU

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
    
    global bot
    bot = application.bot
    
    # Define conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [CallbackQueryHandler(language_selection, pattern='^lang_')],
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)],
            SERVICE_TYPE: [CallbackQueryHandler(service_selection, pattern='^service_')],
            PRINT_FILE: [MessageHandler(filters.Document.FileExtension('stl'), handle_print_file)],
            PRINT_DETAILS: [
                CallbackQueryHandler(handle_material_selection, pattern='^material_'),
                CallbackQueryHandler(handle_color_selection, pattern='^color_'),
                CallbackQueryHandler(handle_strength_selection, pattern='^strength_'),
                CallbackQueryHandler(handle_temperature_selection, pattern='^temp_'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_quantity)
            ],
            MODELING_DESC: [
                MessageHandler(filters.TEXT | filters.PHOTO | filters.Document.ALL, handle_modeling_description)
            ],
            SCANNING_DESC: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_scanning_description)
            ],
            CONTACT_INFO: [
                MessageHandler(filters.CONTACT, handle_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_deadline),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_chat=False
    )
    
    application.add_handler(conv_handler)
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
