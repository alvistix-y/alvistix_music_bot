import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 **မင်္ဂလာပါ! သီချင်းနားထောင်နိုင်သော Bot မှ ကြိုဆိုပါတယ်။**\n\n"
        "ကြိုက်တဲ့ **သီချင်းနာမည်** (သို့) **YouTube Link** ကို ပို့ပေးလိုက်ပါ။ "
        "Bot က သီချင်းဖိုင် (MP3) အဖြစ် ပြောင်းလဲပေးပို့ပါမည်။"
    )

async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=f"🔍 '{query}' ကို ရှာဖွေနေပါပြီ ခဏစောင့်ပါ...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
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
            await context.bot.send_audio(chat_id=chat_id, audio=audio_file, title=title)
        
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ သီချင်းဒေါင်းလုပ်ဆွဲရာတွင် အမှားဖြစ်သွားပါပြီ။ အခြားနာမည်ဖြင့် ထပ်ကြိုးစားပါ။")

def main():
    if not TOKEN:
        return
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_music))
    app.run_polling()

if __name__ == '__main__':
    main()
