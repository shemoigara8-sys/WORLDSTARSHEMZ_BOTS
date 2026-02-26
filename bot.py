import os
import csv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# ==============================
# CONFIG
# ==============================

TOKEN = os.environ.get("TOKEN") or "8610962396:AAFmNiyW9shHT34w99RUUI30GOhKyudLdx8"

# ⚠️ Replace with your real Telegram numeric ID
ADMIN_ID = int(os.environ.get("ADMIN_ID") or 6764405064 )

NAME, TITLE, SKILLS, EDUCATION, EXPERIENCE, LOCATION, EMAIL, GOALS, PHOTO, PAYMENT = range(10)

# ==============================
# SAVE CLIENT DATA
# ==============================

def save_client_folder(data):
    folder_name = data["name"].replace(" ", "_")

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    csv_path = os.path.join(folder_name, "profile.csv")

    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Title", "Skills", "Education", "Experience", "Location", "Email", "Goals"])
        writer.writerow([
            data.get("name", ""),
            data.get("title", ""),
            data.get("skills", ""),
            data.get("education", ""),
            data.get("experience", ""),
            data.get("location", ""),
            data.get("email", ""),
            data.get("goals", "")
        ])

# ==============================
# START COMMAND
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id == ADMIN_ID:
        await update.message.reply_text(
            "👑 ADMIN PANEL\n\n"
            "Commands:\n"
            "/approve <user_id>\n"
            "/reject <user_id>"
        )
        return ConversationHandler.END

    context.user_data.clear()

    await update.message.reply_text(
        "🔥 Welcome to WorldStarShemz Profile Builder 🔥\n\n"
        "What is your full name?"
    )
    return NAME

# ==============================
# CONVERSATION STEPS
# ==============================

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Your current job title?")
    return TITLE

async def title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text
    await update.message.reply_text("List your top skills:")
    return SKILLS

async def skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["skills"] = update.message.text
    await update.message.reply_text("Your education background?")
    return EDUCATION

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["education"] = update.message.text
    await update.message.reply_text("Your work experience?")
    return EXPERIENCE

async def experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["experience"] = update.message.text
    await update.message.reply_text("Your location?")
    return LOCATION

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["location"] = update.message.text
    await update.message.reply_text("Your email address?")
    return EMAIL

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text
    await update.message.reply_text("What are your career goals?")
    return GOALS

async def goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["goals"] = update.message.text
    await update.message.reply_text("Send your LinkedIn profile photo.")
    return PHOTO

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("Please send a photo.")
        return PHOTO

    photo_file = await update.message.photo[-1].get_file()
    filename = f"{context.user_data['name'].replace(' ', '_')}.jpg"
    await photo_file.download_to_drive(filename)

    context.user_data["photo"] = filename

    save_client_folder(context.user_data)

    summary = f"""
🔥 NEW CLIENT SUBMISSION 🔥

User ID: {update.effective_user.id}
Name: {context.user_data['name']}
Title: {context.user_data['title']}
Skills: {context.user_data['skills']}
Education: {context.user_data['education']}
Experience: {context.user_data['experience']}
Location: {context.user_data['location']}
Email: {context.user_data['email']}
Goals: {context.user_data['goals']}
"""

    await context.bot.send_message(chat_id=ADMIN_ID, text=summary)
    await context.bot.send_photo(chat_id=ADMIN_ID, photo=open(filename, "rb"))

    payment_options = [["1️⃣ Send Money"], ["2️⃣ Till Number"], ["3️⃣ Bank Transfer"]]
    reply_markup = ReplyKeyboardMarkup(payment_options, one_time_keyboard=True)

    await update.message.reply_text(
        "✅ Details received.\n\n💰 Service Fee: Ksh 2,000\n\nChoose payment option:",
        reply_markup=reply_markup
    )

    return PAYMENT

# ==============================
# PAYMENT STEP
# ==============================

async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "Send Money" in text:
        await update.message.reply_text(
            "Send Ksh 2,000 to:\n📱 0719369552\nName: WorldStarShemz\n\nAfter payment, paste confirmation message."
        )
        return PAYMENT

    if "Till" in text:
        await update.message.reply_text("Till number not available. Use Send Money option.")
        return PAYMENT

    if "Bank" in text:
        await update.message.reply_text("Bank details will be provided by admin.")
        return PAYMENT

    # Assume payment proof
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"💰 Payment Proof:\n\n{text}")
    await update.message.reply_text("✅ Payment received. Admin will confirm shortly.")

    return PAYMENT

# ==============================
# APPROVE / REJECT COMMANDS
# ==============================

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Not authorized.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /approve <user_id>")
        return

    user_id = int(context.args[0])

    await context.bot.send_message(chat_id=user_id, text="🎉 Your profile has been approved!")
    await update.message.reply_text("✅ User approved.")

async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Not authorized.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /reject <user_id>")
        return

    user_id = int(context.args[0])

    await context.bot.send_message(chat_id=user_id, text="❌ Your submission was rejected. Contact admin.")
    await update.message.reply_text("🚫 User rejected.")

# ==============================
# RUN BOT
# ==============================

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, title)],
        SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, skills)],
        EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, education)],
        EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, experience)],
        LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, location)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
        GOALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, goals)],
        PHOTO: [MessageHandler(filters.PHOTO, photo)],
        PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, payment)],
    },
    fallbacks=[CommandHandler("start", start)],
)

app.add_handler(conv_handler)
app.add_handler(CommandHandler("approve", approve))
app.add_handler(CommandHandler("reject", reject))

app.run_polling()
