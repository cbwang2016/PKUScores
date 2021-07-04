import requests
import time
import telegram

TIMEOUT = 5  # seconds
TGTOKEN = "BOT_TOKEN"
uid = 1234556
PKUHELPER_TOKEN="PKUHELPER_TOKEN"

CHANGE_STATE_THRESHOLD = 3

bot = telegram.Bot(TGTOKEN)

old_msg = ""
connected = 0
state_count = 0
while True:
    try:
        r = requests.get(
            "https://pkuhelper.pku.edu.cn/api_xmcp/isop/scores?user_token=" + PKUHELPER_TOKEN + "&auto=no",
            timeout=TIMEOUT)
        if r.json()['success'] != True:
            raise Exception("TODO")
        msg = "\n".join(["{} {}".format(i["kcmc"], i["xqcj"])
                         for i in r.json()['cjxx'] if i["xnd"] == "20-21" and i["xq"] == "2"])
    except:
        if connected == 0:
            state_count = 0
        else:
            state_count += 1
            if state_count == CHANGE_STATE_THRESHOLD:
                connected = 0
                bot.send_message(chat_id=uid, text="Disconnected.")
    else:
        if connected == 1:
            state_count = 0
        else:
            state_count += 1
            if state_count == CHANGE_STATE_THRESHOLD:
                connected = 1
                bot.send_message(chat_id=uid, text="Connected.")

        if old_msg == "":
            old_msg = msg
            bot.send_message(
                chat_id=uid, text="Bot started.\n" + msg)
            print("Bot started.\n" + msg)
        elif msg != old_msg:
            old_msg = msg
            bot.send_message(chat_id=uid, text=msg)
    time.sleep(60)
