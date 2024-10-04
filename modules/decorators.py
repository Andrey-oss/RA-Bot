from functools import wraps
from datetime import datetime

def id_checker(bot, user_id, log):
    def decorator(func):
        @wraps(func)
        def wrapper(message):
                if message.from_user.id in user_id:
                    return func(message)
                elif log == 1:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Unauthorized user as ID: ", message.chat.id)
                bot.reply_to(message, "Unauthorized access")
        return wrapper
    return decorator

def log_decorator(log):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            message = args[0]
            if log == 1:
                command = message.text
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] User sent command: '{command}'")
            return func(*args, **kwargs)
        return wrapper
    return decorator