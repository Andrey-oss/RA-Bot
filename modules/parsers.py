import json

def config():
    try:
        with open("configs/config.json", "r+") as cfg:
            cfg = json.load(cfg)
    except Exception:
        print ("[-] Cannot open config.json file!")
        exit()
    else:
        return cfg

def commands():
    try:
        with open("configs/commands.json", "r+") as file:
            cmd = json.load(file)
    except Exception:
        print ("[-] Cannot open commands.json file")
        exit()
    else:
        return cmd
