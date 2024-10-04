from modules.parsers import config

__VERSION='1.0.0-beta'

debug = config()['enable_debugging']

try:
    from playsound import playsound
    from datetime import datetime
    from PIL import ImageGrab
    import subprocess
    import speedtest
    import requests
    import psutil
    import cv2
    import os
    import shutil
except Exception as e:
    if debug == 1:
        print(e)
    print("WARNING: Some libraries are missing on this system")

def screenshot(bot, chat_id):
    msg = bot.send_message(chat_id, "Creating screenshot...")
    screenshot = ImageGrab.grab()
    bot.edit_message_text("Saving...", chat_id, message_id=msg.message_id)

    try:
        screenshot.save("cache/screenshot.png")
    except Exception as e:
        if debug == 1:
            bot.edit_message_text(a, chat_id, message_id=msg.message_id)
        else:
            bot.edit_message_text(f"Some error occurred!", chat_id, message_id=msg.message_id)

    bot.delete_message(chat_id, message_id=msg.message_id)
    bot.send_photo(chat_id, photo=open('cache/screenshot.png', 'rb'))
    screenshot.close()

def status():
    result = subprocess.run(['uptime'], capture_output=True, text=True)
    return result.stdout if result.stdout else result.stderr

def disk():
    result = subprocess.run(['df', '-h'], capture_output=True, text=True)
    return result.stdout if result.stdout else result.stderr

def poweroff():
    subprocess.run(['poweroff'], capture_output=False, text=False)
    return "Power off..."

def reboot():
    subprocess.run(['reboot'], capture_output=False, text=False)
    return "Reboot"

def run_speedtest(bot, chat_id):
    try:
        st = speedtest.Speedtest()
        
        output = ""

        msg = bot.send_message(chat_id, "Testing internet speed...")
        
        download_speed = st.download() / 1000000  # Convert to Mbps
        upload_speed = st.upload() / 1000000  # Convert to Mbps
        bot.delete_message(chat_id, message_id=msg.message_id)
        output += "Download Speed: {:.2f} Mbps\n".format(download_speed)
        output += "Upload Speed: {:.2f} Mbps".format(upload_speed)
        
        return output
    except Exception as e:
        if debug == 1:
            return e
        return "Some error occurred. Perhaps, you have to see /healthcheck"

def ip():
    r = requests.get("https://ident.me")
    return r.text

def play_audio(file_path, bot, chat_id, message_id):
    bot.send_message(chat_id, f"Playing audio file {file_path}")
    playsound(file_path)
    bot.edit_message_text("Done!", chat_id, message_id)

def cam_photo(bot, chat_id):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Webcam could not be opened.")
    result, image = cam.read()
    if result:
        cv2.imshow("webcam_photo", image)
        cv2.imwrite("cache/webcam_photo.png", image)
        cv2.destroyWindow("webcam_photo")
    else:
        return "Unable to capture image!"
    bot.send_photo(chat_id, photo=open('cache/webcam_photo.png', 'rb'))

def list_iface():
    interfaces = psutil.net_if_addrs()
    output = ""

    for interface_name, addresses in interfaces.items():
        output += f"🖥 Interface: {interface_name}\n\n"
        for address in addresses:
            output += f"  Address: {address.address}\n"
            output += f"  Family: {address.family}\n"
            output += f"  Mask: {address.netmask}\n"
            output += f"  Broadcast address: {address.broadcast}\n\n"

    return output

def mute():
    try:
        result = subprocess.run(['amixer', 'set', 'Capture', 'nocap'], capture_output=True, text=True)
    except Exception as e:
        if debug == 1:
            return e
        return "Seems like 'alsa-utils' hasn't been installed yet!"
    else:
        if debug == 1:
            return result.stdout if result.stdout else result.stderr
        return "Done!"

def unmute():
    try:
        result = subprocess.run(['amixer', 'set', 'Capture', 'cap'], capture_output=True, text=True)
    except Exception as e:
        if debug == 1:
            return e
        return "Seems like 'alsa-utils' hasn't been installed yet!"
    else:
        if debug == 1:
            return result.stdout if result.stdout else result.stderr
        return "Done!"

def cam_off():
    try:
        result = subprocess.run(['rmmod', '-f', 'uvcvideo'], capture_output=True, text=True)
    except Exception as e:
        if debug == 1:
            return e
        return 'Some error occurred!'
    else:
        if debug == 1:
            return result.stdout if result.stdout else result.stderr
        return "Done!" if result.stdout else "Some error occurred. Perhaps, you should run this bot as root user"

def cam_on():
    try:
        result = subprocess.run(['modprobe', 'uvcvideo'], capture_output=True, text=True)
    except Exception as e:
        if debug == 1:
            return e
        return "Unknown error occurred"
    else:
        if debug == 1:
            if result.stdout:
                return result.stdout
            elif result.stderr:
                return result.stderr
            else:
                return "Command executed with no output"
        return "Done!" if not result.stderr else "Some error occurred. Perhaps, you should run this bot as root user"

def download(file_path, bot, chat_id):
    try:
        f = open(file_path, "rb")
    except Exception:
        return "You have't permission to do that or file doesn't exist"
    else:
        bot.send_document(chat_id, f)
    
def delete(file_path, bot, chat_id):
    try:
        result = subprocess.run(['rm', file_path, "-v"], capture_output=True, text=True)
        if debug == 1:
            return result.stdout if result.stdout else result.stderr
        return "Done!" if result.stdout else "Some error occurred. Perhaps, you should run this bot as root user"
    except Exception as e:
        if debug == 1:
            return e
        return "Some error occurred!"
    else:
        if debug == 1:
            return result.stdout if result.stdout else result.stderr
        return "Done!" if result.stdout else "Some error occurred. Perhaps, you should run this bot as root user"

def usage():
    # RAM
    ram = psutil.virtual_memory()
    ram_total = round(ram[0]/10**9)
    ram_used = round(ram[3]/10**9)
    ram_free = round(ram[4]/10**9)
    # CPU
    cpu = psutil.getloadavg()
    cpu_count = os.cpu_count()
    cpu_load = round((cpu[2]/cpu_count)*100, 2)
    # DISK
    disk = shutil.disk_usage("/")
    disk_total = round(disk[0]/1024**3)
    disk_usage = round(disk[1]/1024**3)
    disk_free = round(disk[2]/1024**3)
    # Processes
    proc_number = len([proc.name() for proc in psutil.process_iter()])
    output = f'''
💿 Disk information:\n
Total size: {disk_total} GB\r
Usage:  {disk_usage} GB\r
Free space: {disk_free} GB\r\n
📱 RAM information:\n
Ram total: {ram_total} GB\r
Usage: {ram_used} GB\r
Free space: {ram_free} GB\r
CPU load: {cpu_load}%\r\n
🖥 Information about processes:\n
Total number of processes: {proc_number}\r
    '''
    return output