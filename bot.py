from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================================
# BOT TOKEN
# =========================================

TOKEN = "8621490477:AAHD4_FBkpS-MVhKyWLhhfd_eCOeYcqXhZI"

# =========================================
# OWNER ID
# =========================================

OWNER_ID = 8621490477

# =========================================
# CHANNEL USERNAMES
# =========================================

CHANNELS = [
    "@techwithtips0",
    "@MoneymasterIndia01",
    "@Visionearner1",
    "@backuptechwithtips"
]

# =========================================
# START COMMAND
# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton(
                "📢 TECH WITH TIPS",
                url="https://t.me/techwithtips0"
            )
        ],

        [
            InlineKeyboardButton(
                "💸 MONEY MASTER",
                url="https://t.me/MoneymasterIndia01"
            )
        ],

        [
            InlineKeyboardButton(
                "🚀 VISION EARNER",
                url="https://t.me/Visionearner1"
            )
        ],

        [
            InlineKeyboardButton(
                "🔰 BACKUP CHANNEL",
                url="https://t.me/backuptechwithtips"
            )
        ],

        [
            InlineKeyboardButton(
                "✅ VERIFY NOW",
                callback_data="verify"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"""
╔══════════════════╗
 ✨ WELCOME TO GAINADDA ✨
╚══════════════════╝

👋 Hello {update.effective_user.first_name}

📢 Join All Channels First

👇 Then Click VERIFY NOW
"""

    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )

# =========================================
# VERIFY FUNCTION
# =========================================

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    user_id = query.from_user.id

    await query.answer("🔍 Verifying...")

    try:

        # CHECK CHANNELS FAST
        for channel in CHANNELS:

            member = await context.bot.get_chat_member(
                channel,
                user_id
            )

            if member.status not in [
                "member",
                "administrator",
                "creator"
            ]:

                await query.answer(
                    "❌ Please Join All Channels First",
                    show_alert=True
                )
                return

        # DELETE OLD MESSAGE
        try:
            await query.message.delete()
        except:
            pass

        # NEW MESSAGE
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"""
✅ Verification Successful

👋 Hello {query.from_user.first_name}

📝 Aapki Problem Kya Hai?

Please Describe Kare 👇
"""
        )

    except Exception as e:

        print(e)

        await query.answer(
            "⚠️ Try Again",
            show_alert=True
        )

# =========================================
# USER MESSAGE
# =========================================

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    text = update.message.text

    # IGNORE COMMANDS
    if text.startswith("/"):

        return

    # USER SUCCESS MESSAGE
    await update.message.reply_text(
        """
✅ Problem Submitted Successfully

📞 Team Will Contact You Soon
"""
    )

    # SEND MESSAGE TO OWNER
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"""
📩 NEW PROBLEM RECEIVED

👤 Name: {user.first_name}

🆔 User ID: {user.id}

📝 Problem:
{text}
"""
    )

# =========================================
# MAIN
# =========================================

app = ApplicationBuilder().token(TOKEN).build()

# START
app.add_handler(
    CommandHandler("start", start)
)

# VERIFY
app.add_handler(
    CallbackQueryHandler(
        verify,
        pattern="verify"
    )
)

# USER MESSAGE
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        user_message
    )
)

print("✅ GainAdda Bot Running Successfully...")

app.run_polling()
