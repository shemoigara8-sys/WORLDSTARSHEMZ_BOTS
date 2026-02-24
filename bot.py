import os
import csv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# 🔑 Use environment variable for token (Railway-friendly)
TOKEN = os.environ.get("TOKEN") or "8610962396:AAFmNiyW9shHT34w99RUUI30GOhKyudLdx8"

# Conversation states
NAME, TITLE, SKILLS, EDUCATION, EXPERIENCE, LOCATION, EMAIL, GOALS, PHOTO = range(9)

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
    if "photo_filename" in data:
        os.rename(data["photo_filename"], os.path.join(folder_name, "photo.jpg"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to WorldStarShemz Bot Services!\n\nWhat is your full name?")
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("What is your current job title?")
    return TITLE

async def title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text
    await update.message.reply_text("List your top skills (comma separated):")
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
    await update.message.reply_text("Almost done! Please send me your profile photo (as an image).")
    return PHOTO

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        name_safe = context.user_data["name"].replace(" ", "_")
        filename = f"{name_safe}_temp.jpg"
        await photo_file.download_to_drive(filename)
        context.user_data["photo_filename"] = filename
        save_client_folder(context.user_data)
        await update.message.reply_text(f"✅ Thank you! Your profile for {context.user_data['name']} is ready.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("⚠️ Please send a photo, not text.")
        return PHOTO

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
    },
    fallbacks=[],
)

app.add_handler(conv_handler)

print("🤖 Bot is running...")
app.run_polling()
