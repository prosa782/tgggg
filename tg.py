import os
import telebot
import yt_dlp

# Bot token
BOT_TOKEN = "7649726493:AAFCTVUzAFtrOiU8b5xAK3xmAPX_yivvDlM"

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Ensure downloads directory exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Function to download YouTube video
def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info_dict)
        return video_path
    except yt_dlp.DownloadError as e:
        return f"DownloadError: {e}"
    except Exception as e:
        return f"General Error: {e}"

# Start command
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a YouTube video URL to download it.")

# Handle YouTube video URLs
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()

    if "youtube.com" in url or "youtu.be" in url:
        bot.reply_to(message, "Downloading YouTube video... Please wait.")
        video_path = download_youtube_video(url)

        if os.path.exists(video_path):
            with open(video_path, "rb") as video:
                bot.send_video(message.chat.id, video)
            os.remove(video_path)  # Clean up after sending
        else:
            bot.reply_to(message, f"Error: {video_path}")
    else:
        bot.reply_to(message, "Please send a valid YouTube video URL.")

# Start the bot
print("Bot is running...")
bot.polling(non_stop=True)