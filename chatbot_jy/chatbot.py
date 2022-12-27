from chatbot_jy.information import *
from konlpy.tag import Okt
from chatbot_jy.get_api_data import *
import pandas as pd
import sys

country_standing_json = get_country_standings()
match_info_json = get_match_info()
today_match_json = get_match_today()
df_pred_all = pd.read_csv('./chatbot_jy/wc_forecasts.csv')
df_pred_match = pd.read_csv('./chatbot_jy/wc_matches.csv')
okt = Okt()

idontknowstr="잘 알아듣지 못했어요~ 대한민국 화이팅!!!"

def chatbot(input_str):
    msg = []

    input_list = okt.nouns(input_str)
    input_list = input_list + input_str.split()

    country_list = []
    
    for tmp_str in input_list:
        for key, value in Participate_Country_dic.items():
            if tmp_str in value:
                country_list.append(key)
                break

    country_list = list(set(country_list))
    #print(country_list)

    # 감지된 나라가 2개이면, 경기 결과를 불러온다.
    if len(country_list) == 2:
        for tmp_str in ["예측", "예상", "확률"]:
            if tmp_str in input_list:
                tmp_data = pred_team_match(df_pred_match, country_list[0], country_list[1])
                if tmp_data == None:
                    msg.append(f"{Participate_Country_dic[country_list[0]][0]}와 {Participate_Country_dic[country_list[1]][0]}의 경기는 없습니다.")
                else:
                    msg.append(f"{Participate_Country_dic[tmp_data[0]][0]}의 승리 확률은 {tmp_data[2]*100}%, {Participate_Country_dic[tmp_data[1]][0]}의 승리 확률은 {tmp_data[3]*100}%, 무승부 확률은 {tmp_data[4]*100}% 입니다.")
                return msg
                
        for tmp_str in ["결과", "승패"]:
            if tmp_str in input_list:
                # 경기 승패 불러오기
                tmp_data = get_match_score(match_info_json, country_list[0], country_list[1])
                if tmp_data == None:
                    msg.append(f"{Participate_Country_dic[country_list[0]][0]}와 {Participate_Country_dic[country_list[1]][0]}의 경기는 아직 진행되지 않았습니다.")
                else:
                    #get time
                    time = get_kst_time(tmp_data)
                    msg.append(f"{Participate_Country_dic[tmp_data['homeTeam']['name']][0]}와 {Participate_Country_dic[tmp_data['awayTeam']['name']][0]}의 경기 결과는 {tmp_data['homeTeam']['goals']} : {tmp_data['awayTeam']['goals']}로, KST {' '.join(time)}에 {tmp_data['location']}에서 진행했습니다.")
                return msg
        
        return idontknowstr

    # 감지된 나라가 1개이면, 그 나라의 실적을 불러온다.
    elif len(country_list) == 1:
        for tmp_str in ["예측", "예상", "진출", "확률"]:
            if tmp_str in input_list:
                msg.append(f"{Participate_Country_dic[country_list[0]][0]}의 16강 진출 확률은 {float(df_pred_all[df_pred_all['team'] == country_list[0]]['make_round_of_16'])*100}% 입니다.")
                return msg

        for tmp_str in ["성적", "승패", "점수", "실점", "순위"]:
            if tmp_str in input_list:
                tmp_data = get_country_score(country_standing_json, country_list[0])
                msg.append(f"{Participate_Country_dic[country_list[0]][0]}의 현재 성적은 {tmp_data['points']//3}승 {tmp_data['draws']}무 {tmp_data['losses']}패입니다.\n현재 {tmp_data['points']}점의 점수로 조별 리그 {tmp_data['position']}순위에 위치하고 있습니다.")
                return msg

        return idontknowstr

    elif "오늘" in input_list:
        for tmp_str in ["경기", "일정", "매치"]:
            if tmp_str in input_list:
                msg.append("오늘의 월드컵 경기는 다음과 같습니다.")
                for idx in range(len(today_match_json)):
                    tmp_data = today_match_json[idx]
                    time = get_kst_time(tmp_data)
                    if tmp_data['status'] == 'completed':
                        msg.append(f"{Participate_Country_dic[tmp_data['homeTeam']['name']][0]}와 {Participate_Country_dic[tmp_data['awayTeam']['name']][0]}의 경기 결과는 {tmp_data['homeTeam']['goals']} : {tmp_data['awayTeam']['goals']}로, KST {' '.join(time)}에 {tmp_data['location']}에서 진행되었습니다.")
                    else:
                        msg.append(f"{Participate_Country_dic[tmp_data['homeTeam']['name']][0]}와 {Participate_Country_dic[tmp_data['awayTeam']['name']][0]}의 경기는, KST {' '.join(time)}에 {tmp_data['location']}에서 진행됩니다.")
                return msg

        return idontknowstr

    elif "조" in input_list:
        idx = get_group_name(input_list)
        if idx != -1:
            group_list = list(Group_Info_dic.values())[idx]
            rank_str = ["등팀은", "등팀", "등", "위조", "위팀", "순위", "위"]
            # 1등팀, 1등, 1위조, 1순위, 1위
            for x in range(1, 5):
                for y in range(len(rank_str)):
                    tmp_str = str(x) + rank_str[y]
                    if tmp_str in input_list:
                        for i in range(len(group_list)):
                            tmp_data = get_country_score(country_standing_json, group_list[i])
                            if tmp_data["position"] == x:
                                msg.append(f"{list(Group_Info_dic.keys())[idx]}조 {tmp_data['position']}위 팀은 {Participate_Country_dic[tmp_data['alternateName']][0]}로 현재 {tmp_data['points']//3}승 {tmp_data['draws']}무 {tmp_data['losses']}패입니다")
                                return msg

            return idontknowstr

        return idontknowstr

    else:
        return idontknowstr

if __name__ == "__main__":
    print("카타르 월드컵 챗봇 가동 준비 완료.")

    while True:
        input_str = sys.stdin.readline()
        print(chatbot(input_str))