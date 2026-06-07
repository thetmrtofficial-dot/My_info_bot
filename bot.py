from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, ContextTypes

TOKEN = "8748997422:AAGkqPh6G0Z8DyHeQKos5PntIsvJHFbz_xU"
WAITING_FOR_INPUT = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇮🇳 India Number", callback_data='india'), InlineKeyboardButton("🇵🇰 Pakistan Number", callback_data='pakistan')],
        [InlineKeyboardButton("📞 Truecaller", callback_data='truecaller')],
        [InlineKeyboardButton("🚗 Vehicle", callback_data='vehicle'), InlineKeyboardButton("🏦 IFSC", callback_data='ifsc')],
        [InlineKeyboardButton("📱 IMEI", callback_data='imei'), InlineKeyboardButton("🌐 IP", callback_data='ip')],
        [InlineKeyboardButton("📍 Pincode", callback_data='pincode'), InlineKeyboardButton("🏢 GST", callback_data='gst')],
        [InlineKeyboardButton("📸 Instagram", callback_data='insta'), InlineKeyboardButton("🆔 Aadhaar", callback_data='aadhaar')],
        [InlineKeyboardButton("📡 TG to Number", callback_data='tg_num'), InlineKeyboardButton("💳 PAN Lookup", callback_data='pan')],
        [InlineKeyboardButton("📄 PAN GST", callback_data='pan_gst'), InlineKeyboardButton("🎮 Free Fire ID", callback_data='ff_id')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Select an option:', reply_markup=reply_markup)
    return WAITING_FOR_INPUT

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['choice'] = query.data
    await query.edit_message_text(f"Selected: {query.data.upper()}\nPlease enter the details:")
    return WAITING_FOR_INPUT

async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    choice = context.user_data.get('choice', 'Unknown')
   
    await update.message.reply_text(f"Searching {user_input} in {choice} database...\n\nResult: Processing...")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITING_FOR_INPUT: [
                CallbackQueryHandler(button_click), 
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_info)
            ]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    app.add_handler(conv_handler)
    app.run_polling()
