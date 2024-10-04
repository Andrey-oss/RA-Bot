from modules.parsers import *
from modules.commands import *
from modules.healthcheck import *
from modules.decorators import *
import telebot

user_id = config()['id']  # UserID
api = config()['api_key']  # API key
debug = config()['enable_debugging'] # Enable partial debugging. Useful for developers
log = config()['enable_logging'] # Enable logging into console

bot = telebot.TeleBot(api, parse_mode=None)

checkboot() # Check necessary requirements

@bot.message_handler(commands=['start'])
@log_decorator(log)
@id_checker(bot, user_id, log)
def send_welcome(message):
    bot.send_message(message.chat.id, f"Welcome @{message.from_user.username}! Use '/help' to get all available commands and usage")

@bot.message_handler(commands=['help'])
@log_decorator(log)
@id_checker(bot, user_id, log)
def help(message):
    text = "Available commands:\n"
    for category, cmds in commands().items():
        text += f"\n{category}\n"
        for cmd, details in cmds.items():
            text += f"{cmd} - {details['description']}\nUsage: {details['usage']}\n"

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['healthcheck'])
@log_decorator(log)
@id_checker(bot, user_id, log)
def healthcheck(message):
    bot.send_message(message.chat.id, "Running healthcheck, please wait..")
    result = hcheck(bot, message, debug, log)
    bot.reply_to(message, result)

@bot.message_handler(func=lambda message: message.text.startswith('/'))
@log_decorator(log)
@id_checker(bot, user_id, log)
def handle_command(message):
    parts = message.text.split()
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    for category, cmds in commands().items():
        if command in cmds:
            log_message = bot.send_message(message.chat.id, f"Starting command {command}...")
            response = execute_command(command, args, message.chat.id, log_message.message_id)
            bot.reply_to(message, response)
            return

    bot.reply_to(message, "Unknown command. Use '/help' to see available commands")

def execute_command(command, args, chat_id, message_id):
    try:
        if command == '/uptime':
            return status()
        elif command == '/usage':
            return usage()
        elif command == '/poweroff':
            return poweroff()
        elif command == '/reboot':
            return reboot()
        elif command == '/speedtest':
            return run_speedtest(bot, chat_id)
        elif command == '/ip':
            return ip()
        elif command == '/list_iface':
            return list_iface()
        elif command == '/play':
            if args:
                file_path = args[0]
                return play_audio(file_path, bot, chat_id, message_id)
            else:
                return "Usage: /play <file_path>"
        elif command == '/cam':
            return cam_photo(bot, chat_id)
        elif command == '/screenshot':
            return screenshot(bot, chat_id)
        elif command == '/mute':
            return mute()
        elif command == '/unmute':
            return unmute()
        elif command == '/cam_off':
            return cam_off()
        elif command == '/cam_on':
            return cam_on()
        elif command == '/delete':
            if args:
                file_path = args[0]
                return delete(file_path, bot, chat_id)
            return "Usage: /delete <file_path>"
        elif command == '/download':
            if args:
                file_path = args[0]
                download(file_path, bot, chat_id)
            else:
                return "Usage: /download <file_path>"
        else:
            return "Command not implemented"
    except Exception as e:
        if debug == 1:
            return f"Error executing command: {str(e)}"
        return "Some error ocurred! Perhaps, you have to see the bot's code"

bot.infinity_polling()
