import cv2
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace with your actual configuration details
BOT_TOKEN = "8962958469:AAGUIoym1UZWX_a7NQkaqIwBtHnAg-5Od3w"
AUTHORIZED_CHAT_ID = 8616355757  # Replace with your numeric Chat ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message and lists available commands."""
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    
    await update.message.reply_text(
        "📷 Home Security Camera Bot Active.\n\n"
        "Use /snapshot to receive a live picture from the webcam."
    )

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Captures an image from the webcam and sends it to the authorized chat."""
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return

    # Notify user that the request is processing
    status_msg = await update.message.reply_text("🔄 Accessing camera hardware...")

    # Initialize the primary system webcam (0)
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        await status_msg.edit_text("❌ Error: Could not access the webcam device.")
        return

    # Warm up camera sensor and read a single frame
    for _ in range(5):
        video_capture.read()
    success, frame = video_capture.read()
    video_capture.release()

    if success:
        # Save image locally
        image_path = "live_snapshot.jpg"
        cv2.imwrite(image_path, frame)
        
        # Send image file back via Telegram
        await status_msg.delete()
        with open(image_path, "rb") as photo_file:
            await update.message.reply_photo(photo=photo_file, caption="📸 Live Snapshot")
    else:
        await status_msg.edit_text("❌ Error: Failed to capture frame from camera.")

def main():
    """Initializes and runs the Telegram bot application."""
    # Create the application with your bot token
    app = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("snapshot", snapshot))

    # Start polling for messages
    print("Bot is polling... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
