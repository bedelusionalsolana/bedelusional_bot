import os
import io
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image, ImageDraw, ImageFont, ImageFilter

async def be_delusional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("Reply to a photo with /bedelusional.")
        return

    # Download image from Telegram
    photo = update.message.reply_to_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = await file.download_as_bytearray()

    # Open and grayscale image, apply dark tint
    image = Image.open(io.BytesIO(photo_bytes)).convert("L").convert("RGBA")
    black_overlay = Image.new("RGBA", image.size, (0, 0, 0, 120))
    image = Image.alpha_composite(image, black_overlay)

    # Crop image to center square
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    image = image.crop((left, top, left + side, top + side))

    # Prepare text
    draw = ImageDraw.Draw(image)
    text = "BE DELUSIONAL"
    font_path = Path(__file__).parent / "fonts" / "arialbd.ttf"
    font_size = int(image.width * 0.2)

    # Fit text within 85% of image width
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

    # Create blurred glow layer
    glow_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.text((x, y), text, font=font, fill=(255, 0, 0, 255))
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=4))

    # Composite glow and base image
    image = Image.alpha_composite(image, blurred_glow)

    # Draw final crisp red text
    draw = ImageDraw.Draw(image)
    draw.text((x, y), text, font=font, fill=(255, 0, 0, 255))

    # Send back the edited image
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
