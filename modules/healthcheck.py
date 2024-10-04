import os
import pkg_resources
import sys
import platform

def checkboot():
    '''
    Check at starting necessary requirements. If some test/s will be failed, you have WARNING ONLY!
    '''
    if os.getuid() != 0:
        print("WARNING: The bot has been run as non-root user! Some commands can't be executed")
    if os.uname().sysname != 'Linux':
        print("WARNING: Incompatible system. Please read the README.md before running! Functionality could be limited")

def hcheck(bot, message, debug, log):
    '''
    Use if you wish to check your all requirements about bot 
    '''
    output = ""
    msg = None

    def system_info():
        nonlocal msg
        msg = bot.send_message(message.chat.id, "Getting system information")
        nonlocal output
        output = f"🖥 System informarion: \n💻 OS: {platform.system()}\n📝 Version: {platform.version()}\n⚡ Bit: {platform.machine()}\n\n"

    def get_user():
        nonlocal msg
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Getting user information")
        nonlocal output
        output += f"🖥 User information: \n🧑‍💻 User - {os.getlogin()}\n📂 Group - {os.getuid()}\n\n"
    
    def py_ver():
        nonlocal msg
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Getting python version")
        nonlocal output
        version = sys.version_info
        output += f"🖥 Environment: \n🐍 Python version: {version.major}.{version.minor}.{version.micro}\n\n"
    
    def check_py_deps():
        nonlocal msg
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Checking python dependencies")
        nonlocal output
        output += "🖥 Python dependencies: \n"
        
        with open('requirements.txt', 'r') as f:
            dependencies = f.read().splitlines()

        for dep in dependencies:
            dep = dep.strip()
            if dep:
                try:
                    pkg_resources.require(dep)
                    output += f"✅ Package '{dep}' is installed and up-to-date\n"
                except pkg_resources.DistributionNotFound:
                    output += f"❌ Package '{dep}' is not installed\n"
                except pkg_resources.VersionConflict as e:
                    output += f"⚠ Package '{dep}' is installed but the version is different: {e.report()}\n"
    
    def check_settings():
        nonlocal msg
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Checking settings")
        nonlocal output
        output += "\n⚙️ Bot settings\n"
        if debug == 1:
            output += "✅ Debugging: Enabled\n"
        else:
            output += "❌ Debugging: Disabled\n"
        if log == 1:
            output += "✅ Logging: Enabled\n"
        else:
            output += "❌ Logging: Disabled\n"
    
    system_info()
    get_user()
    py_ver()
    check_py_deps()
    check_settings()

    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    
    return output