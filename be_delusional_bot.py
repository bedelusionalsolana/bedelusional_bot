import os
import io
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image, ImageDraw, ImageFont

async def sexy_solana_summer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("Reply to a photo with /sss.")
        return

    # Download the replied photo
    photo = update.message.reply_to_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = await file.download_as_bytearray()

    # Step 1: Open, grayscale, darken
    image = Image.open(io.BytesIO(photo_bytes)).convert("L").convert("RGBA")
    black_overlay = Image.new("RGBA", image.size, (0, 0, 0, 120))
    image = Image.alpha_composite(image, black_overlay)

    # Step 2: Crop to square (1:1)
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    right = left + side
    bottom = top + side
    image = image.crop((left, top, right, bottom))

    # Step 3: Load logo
    logo_path = Path(__file__).parent / "assets" / "TEXTSAA.png"
    logo = Image.open(str(logo_path)).convert("RGBA")

    # Resize logo to 70% of image width, keep aspect ratio
    target_width = int(image.width * 0.7)
    aspect_ratio = logo.width / logo.height
    target_height = int(target_width / aspect_ratio)
    logo = logo.resize((target_width, target_height), Image.LANCZOS)

    # Step 4: Center the logo
    x = (image.width - logo.width) // 2
    y = (image.height - logo.height) // 2
    image.paste(logo, (x, y), logo)  # use logo as its own transparency mask

    # Step 5: Send it back
    output = io.BytesIO()
    image.convert("RGB").save(output, format="JPEG")
    output.seek(0)
    await update.message.reply_photo(photo=output, caption="Sexy Solana Summer 🌞")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm alive. Reply to a photo with /sss.")

def main():
    token = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sss", sexy_solana_summer))
    app.run_polling()

if __name__ == "__main__":
    main()
