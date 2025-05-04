import os
import io
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image, ImageDraw, ImageFont

async def be_delusional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("Reply to a photo with /bedelusional.")
        return

    # Get the image file from the replied message
    photo = update.message.reply_to_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = await file.download_as_bytearray()

    # Open and convert to grayscale with alpha channel
    image = Image.open(io.BytesIO(photo_bytes)).convert("L").convert("RGBA")

    # Apply dark black overlay
    black_overlay = Image.new("RGBA", image.size, (0, 0, 0, 120))
    image = Image.alpha_composite(image, black_overlay)

    # Draw the text
    draw = ImageDraw.Draw(image)
    text = "BE DELUSIONAL"
    font_size = int(image.width * 0.13)  # Bigger font based on image width

    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)  # Bold font
    except:
        font = ImageFont.load_default()

    # Center the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2

    # Add red glow shadow
    shadow_color = (255, 0, 0, 100)
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            draw.text((x + dx, y + dy), text, font=font, fill=shadow_color)

    # Final red text
    draw.text((x, y), text, font=font, fill=(255, 0, 0, 255))

    # Save edited image and send
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
