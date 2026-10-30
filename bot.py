import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 မင်္ဂလာပါ! သီချင်းနားထောင်နိုင်သော Bot မှ ကြိုဆိုပါတယ်။\n"
        "ကြိုက်နှစ်သက်သော **သီချင်းနာမည်** (သို့) **YouTube လင့်ခ်** ကို ပို့ပေးပါ။\n"
        "Bot က သီချင်းဖိုင် (MP3) အဖြစ် ပြောင်းလဲပေးပါမည်။"
    )

async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    chat_id = update.effective_chat.id
    
    await context.bot.send_message(chat_id=chat_id, text="🔍 သီချင်းကို ရှာဖွေနေပါပြီ၊ ခဏစောင့်ပါ...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'tv_embedded']  # YouTube ၏ Bot ကန့်သတ်ချက်ကို ကျော်လွှားရန်
            }
        },
        'cookiefile': 'm.youtube.com_cookies.txt',  # Cookie ဖိုင်ချိတ်ဆက်ခြင်း
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'song.%(ext)s',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if not query.startswith("http"):
                search_query = f"ytsearch1:{query}"
                info = ydl.extract_info(search_query, download=True)
                if 'entries' in info:
                    info = info['entries'][0]
            else:
                info = ydl.extract_info(query, download=True)

            filename = "song.mp3"
            title = info.get('title', 'Music Audio')

        with open(filename, 'rb') as audio_file:
            await context.bot.send_audio(
                chat_id=chat_id,
                audio=audio_file,
                title=title
            )

    except Exception as e:
        logging.error(f"Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text=f"❌ သီချင်းဒေါင်းလုပ်ဆွဲရာတွင် အမှားအယွင်းရှိနေပါသည်: {e}")

    finally:
        if os.path.exists("song.mp3"):
            os.remove("song.mp3")

if __name__ == '__main__':
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable is missing!")
        
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_music))

    print("Bot is running...")
    application.run_polling()
    g
