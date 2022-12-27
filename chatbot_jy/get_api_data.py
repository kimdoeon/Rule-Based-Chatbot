import requests
import json

def get_country_standings():
    requestData = requests.get('https://copa22.medeiro.tech/groups')
    jsonData = None

    if requestData.status_code == 200 :
        jsonData = requestData.json()

    return jsonData

def get_match_info():
    requestData = requests.get('https://copa22.medeiro.tech/matches')
    jsonData = None

    if requestData.status_code == 200 :
        jsonData = requestData.json()

    return jsonData

def get_match_today():
    requestData = requests.get('https://copa22.medeiro.tech/matches/today')
    jsonData = None

    if requestData.status_code == 200 :
        jsonData = requestData.json()

    return jsonData

def get_country_score(jsondata, country_name):
    for idx in range(len(jsondata)):
        if 'teams' in jsondata[idx]:
            for idx2 in range(len(jsondata[idx]['teams'])):
                if jsondata[idx]['teams'][idx2]['alternateName'] == country_name:
                    return(jsondata[idx]['teams'][idx2])
    return None

def get_match_score(jsondata, name1, name2):
    for idx in range(len(jsondata)):
        if jsondata[idx]['status'] == 'completed':
            if jsondata[idx]['homeTeam']['name'] == name1 and jsondata[idx]['awayTeam']['name'] == name2:
                return jsondata[idx]
            if jsondata[idx]['homeTeam']['name'] == name2 and jsondata[idx]['awayTeam']['name'] == name1:
                return jsondata[idx]
    return None

def pred_team_match(df_pred_match, t1, t2):
    for i in range(len(df_pred_match)):
        df_pred_tmp = df_pred_match.iloc[i]
        if df_pred_tmp["team2"] == t1 and df_pred_tmp["team1"] == t2:
            return df_pred_tmp['team1'], df_pred_tmp['team2'], df_pred_tmp['prob1'], df_pred_tmp['prob2'], df_pred_tmp['probtie']

        if df_pred_tmp["team1"] == t1 and df_pred_tmp["team2"] == t2:
            return df_pred_tmp['team1'], df_pred_tmp['team2'], df_pred_tmp['prob1'], df_pred_tmp['prob2'], df_pred_tmp['probtie']

    return None

def get_kst_time(tmp_data):
    time = tmp_data['date'].split('T')
    time[1] = time[1][:5]
    adddate = (int(time[1][:2]) + 9)//24
    if adddate:
        time[0] = time[0][:8] + str(int(time[0][8:])+adddate)
    time[1] = str((int(time[1][:2]) + 9)%24)+ time[1][2:]
    return time

def get_group_name(input_list):
    group_list = ["A조", "B조", "C조", "D조", "E조", "F조", "G조", "H조"]
    group_list2 = ["a조", "b조", "c조", "d조", "e조", "f조", "g조", "h조"]
    for tmp_str in input_list:
        for i in range(len(group_list)):
            if tmp_str == group_list[i] or tmp_str == group_list2[i]:
                return i
    return -1