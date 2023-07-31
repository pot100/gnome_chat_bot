from Django import Django, CI
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from dotenv import load_dotenv

# Load environment variables from KEY.ENV
load_dotenv("KEY.ENV")

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = 'YOUR_ORGANIZATION_ID'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Welcome to the intelligent bot.")

def help_command(update, context):
    commands = [
        "/start - Start the chat bot",
        "/help - Show a list of all commands",
        "/new - Start a new chat session",
        "/mode - Select chat mode",
        "/retry - Regenerate response for the previous query"
    ]
    context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(commands))

def new_chat(update, context):
    # Logic to handle starting a new chat session
    context.bot.send_message(chat_id=update.effective_chat.id, text="Starting a new chat session...")

def select_mode(update, context):
    # Logic to handle selecting chat mode
    context.bot.send_message(chat_id=update.effective_chat.id, text="Selecting chat mode...")

def retry(update, context):
    # Logic to handle regenerating response for previous query
    context.bot.send_message(chat_id=update.effective_chat.id, text="Regenerating response for the previous query...")

def echo(update, context):
    # Use OpenAI API to generate a response
    response = openai.Completion.create(
        engine='davinci',
        prompt=update.message.text,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=response.choices[0].text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Create an instance of Updater with your bot token.
    updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)

    # Get the dispatcher.
    dp = updater.dispatcher

    # Set command handler for the /start command.
    dp.add_handler(CommandHandler("start", start))

    # Set command handler for the /help command.
    dp.add_handler(CommandHandler("help", help_command))

    # Set command handler for the /new command.
    dp.add_handler(CommandHandler("new", new_chat))

    # Set command handler for the /mode command.
    dp.add_handler(CommandHandler("mode", select_mode))

    # Set command handler for the /retry command.
    dp.add_handler(CommandHandler("retry", retry))

    # Set message handler to respond to user messages.
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Set error handler.
    dp.add_error_handler(error)

    # Start the bot.
    updater.start_polling()

    # Get the bot username.
    bot_username = updater.bot.username

    # Run the bot until Ctrl+C is pressed.
    updater.idle()

if __name__ == '__main__':
    main()
