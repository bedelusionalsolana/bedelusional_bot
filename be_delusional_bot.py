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

    photo = update.message.reply_to_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = await file.download_as_bytearray()

    # Step 1: Convert to grayscale + dark overlay
    image = Image.open(io.BytesIO(photo_bytes)).convert("L").convert("RGBA")
    black_overlay = Image.new("RGBA", image.size, (0, 0, 0, 120))
    image = Image.alpha_composite(image, black_overlay)

    # Step 2: Center crop to square
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    image = image.crop((left, top, left + side, top + side))

    # Step 3: Prepare text
    draw = ImageDraw.Draw(image)
    text = "BE DELUSIONAL"
    font_path = Path(__file__).parent / "fonts" / "arialbd.ttf"
    font_size = int(image.width * 0.2)

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

    text_height = bbox[3] - bbox[1]
    x = (image.width - text_width) / 2
    y = int(image.height * 0.6 - text_height / 2)

    # Step 4: Red glow effect
    glow_color = (255, 0, 0, 160)
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            draw.text((x + dx, y + dy), text, font=font, fill=glow_color)

    # Step 5: Final red text
    draw.text((x, y), text, font=font, fill=(255, 0, 0, 255))

    # Step 6: Save and send
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
