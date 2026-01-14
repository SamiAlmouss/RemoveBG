import os
from rembg import remove
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler, ContextTypes,filters

TOKEN = '8409955360:AAF-Pij4NJJ7FkiGmRmDUFg-OVQ-rqN-0f0'

async def help_func(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=update.effective_chat.id,text="Hallo Sami ! Click auf /Start   --> to Starting !!")

async def start_func(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=update.effective_chat.id,text="To remove a background form an image, please send me the image")

async  def process_image(photo_name:str):
    name,_ = os.path.splitext(photo_name)
    output_photo_path = f'./processed/{name}.png'
    my_input = Image.open(f'./temp/{photo_name}')
    my_output = remove(my_input)
    my_output.save(output_photo_path)
    os.remove(f'./temp/{photo_name}')
    return output_photo_path

async  def msg_func(update: Update,context: ContextTypes.DEFAULT_TYPE):
    photo_name=''
    file_id=''
    if filters.PHOTO.check_update(update):
        file_id = update.message.photo[-1].file_id
        unique_file_id = update.message.photo[-1].file_unique_id
        photo_name = f'{unique_file_id}.jpg'

    elif filters.Document.IMAGE:
        file_id = update.message.document.file_id
        _,f_ext = os.path.splitext(update.message.document.file_name)
        unique_file_id = update.message.document.file_unique_id
        photo_name = f'{unique_file_id}.{f_ext}'

    photo_file = await context.bot.getFile(file_id)
    await photo_file.download_to_drive(custom_path=f'./temp/{photo_name}')
    await context.bot.sendMessage(chat_id=update.effective_chat.id,text = 'We are processing your photo . Please wait...')
    processed_image = await process_image(photo_name)
    await context.bot.sendDocument(chat_id=update.effective_chat.id,document=processed_image)
    os.remove(processed_image)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    help_handler = CommandHandler('help',  help_func)
    start_handler = CommandHandler('start', start_func)
    message_handler = MessageHandler(filters.PHOTO | filters.Document.IMAGE, msg_func)

    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    print("Your Bot Is Started ...")
    application.run_polling()

if __name__=="__main__":
    main()




