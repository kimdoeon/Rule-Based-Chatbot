from chatbot_du import match_info as chatbot_du
from chatbot_jy import chatbot as chatbot_jy
from chatbot_sy import chatbot_wc as chatbot_sy
from chatbot_yw import main as chatbot_yw
import pandas as pd
from konlpy.tag import Okt
import sys
import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters

token = '5964232752:AAEHZWMHpUPKltnX0jDLw_lUP0QEGuUViog'
id = "5723762115"

bot = telegram.Bot(token = token)

idontknowstr="잘 알아듣지 못했어요~ 대한민국 화이팅!!!"
# updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()
bot.sendMessage(chat_id = id,text = "2022 카타르 월드컵 챗봇입니다:)\n질문 내용을 입력하세요.")

chatbot_du.crawling_match_info()

def handler(update, context):
    
    input_str = update.message.text
    
#--------------------- <chat JY> ---------------------
    return_state = chatbot_jy.chatbot(input_str)
    if return_state != idontknowstr:
        # print("JY")
        if  str(type(return_state)) == "<class 'list'>":
            bot.sendMessage(chat_id = id,text = '\n'.join(return_state))
        else:
            bot.sendMessage(chat_id = id,text = return_state)

#--------------------- <chat DU> ---------------------
    if return_state == idontknowstr:
        return_state = chatbot_du.chatbot(input_str)
        if return_state != idontknowstr:
            # print("DU")
            if  str(type(return_state)) == "<class 'list'>":
                bot.sendMessage(chat_id = id,text = '\n'.join(return_state))
            else:
                bot.sendMessage(chat_id = id,text = return_state)

#--------------------- <chat SY> ---------------------
    if return_state==idontknowstr:
        return_state = chatbot_sy.chatbot(input_str)
        if return_state != idontknowstr:
            # print("SY")
            if str(type(return_state)) == "<class 'list'>":
                bot.sendMessage(chat_id = id,text = '\n'.join(return_state))
            else:
                bot.sendMessage(chat_id=id, text = idontknowstr)

#--------------------- <chat YW> ---------------------
    if return_state == idontknowstr:
        return_state = chatbot_yw.player_team_all(input_str)
        if return_state != idontknowstr:
            # print("YW")
            if str(type(return_state)) == "<class 'list'>":
                bot.sendMessage(chat_id = id,text = ' '.join(return_state))
            else:
                bot.sendMessage(chat_id=id, text = idontknowstr)

#-----------------------------------------------------
    if return_state ==idontknowstr:
        bot.sendMessage(chat_id=id, text = idontknowstr)

echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)