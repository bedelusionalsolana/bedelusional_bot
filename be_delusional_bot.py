import os
import io
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image, ImageDraw, ImageFont

async def be_delusional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("Reply to a photo with /bedelusional.")
        return

    # Download the replied photo
    photo = update.message.reply_to_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = await file.download_as_bytearray()

    # Open image in grayscale and apply dark overlay
    image = Image.open(io.BytesIO(photo_bytes)).convert("L").convert("RGBA")
    black_overlay = Image.new("RGBA", image.size, (0, 0, 0, 120))
    image = Image.alpha_composite(image, black_overlay)

    # Crop image to square (centered 1:1)
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    right = left + side
    bottom = top + side
    image = image.crop((left, top, right, bottom))

    # Prepare text and font
    draw = ImageDraw.Draw(image)
    text = "BE DELUSIONAL"
    font_path = Path(__file__).parent / "fonts" / "arialbd.ttf"
    font_size = int(image.width * 0.2)

    # Dynamically adjust font size to fit within 85% width
    while True:
        try:
            font = ImageFont.truetype(str(font_path), font_size)
        except:
            font = ImageFont.load_default()
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        if text_width <= image.width * 0.85:
            break
        font_size -= 2

    # Position text slightly lower than center (around 60% height)
    text_height = bbox[3] - bbox[1]
    x = (image.width - text_width) / 2
    y = int(image.height * 0.6 - text_height / 2)

    # Red glow
    glow_color = (255, 0, 0, 100)
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            draw.text((x + dx, y + dy), text, font=font, fill=glow_color)

    # Final red text
    draw.text((x, y), text, font=font, fill=(255, 0, 0, 255))

    # Save and reply
    output = io.BytesIO()
    image.convert("RGB").save(output, format="JPEG")
    output.seek(0)
    await update.message.reply_photo(photo=output, caption="BE DELUSIONAL.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm alive. Reply to a photo with /bedelusional.")

def main():
    token = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bedelusional", be_delusional))
    app.run_polling()

if __name__ == "__main__":
    main()
