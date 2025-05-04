import os
import io
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image, ImageDraw, ImageFont

async def be_delusional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("Reply to a photo with /bedelusional.")
        return

    # Get the photo from the replied message
    photo = update.message.reply_to_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = await file.download_as_bytearray()

    # Open the image and apply black & white filter
    image = Image.open(io.BytesIO(photo_bytes)).convert("L").convert("RGBA")

    # Add dark overlay
    black_overlay = Image.new('RGBA', image.size, (0, 0, 0, 120))  # semi-transparent black
    image = Image.alpha_composite(image, black_overlay)

    # Draw the red text
    draw = ImageDraw.Draw(image)
    font_size = int(image.width / 2.5)

    try:
        # Use bold font if available
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except:
        font = ImageFont.load_default()

    text = "BE DELUSIONAL"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2
    draw.text((x, y), text, font=font, fill=(255, 0, 0, 255))

    # Convert to JPEG and send back
    output = io.BytesIO()
    image.convert("RGB").save(output, format="JPEG")
    output.seek(0)

    await update.message.reply_photo(photo=output, caption="be delusional.")

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
