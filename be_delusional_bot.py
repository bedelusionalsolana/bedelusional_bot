import os
import io
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image, ImageDraw, ImageFont

async def be_delusional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("Reply to a photo with /bedelusional.")
        return

    # Get the photo
    photo = update.message.reply_to_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = await file.download_as_bytearray()

    # Edit the image
    image = Image.open(io.BytesIO(photo_bytes)).convert("L").convert("RGBA")
    black_overlay = Image.new('RGBA', image.size, (0, 0, 0, 100))
    image = Image.alpha_composite(image, black_overlay)

    draw = ImageDraw.Draw(image)
    font_size = int(min(image.size) / 8)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    text = "BE DELUSIONAL"
    text_width, text_height = draw.textsize(text, font=font)
    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2
    draw.text((x, y), text, font=font, fill=(255, 0, 0, 255))

    output = io.BytesIO()
    image.convert("RGB").save(output, format="JPEG")
    output.seek(0)

    await update.message.reply_photo(photo=output, caption="be delusional.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm alive!")

def main():
    token = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bedelusional", be_delusional))
    app.run_polling()

if __name__ == "__main__":
    main()
