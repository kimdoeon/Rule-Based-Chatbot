#정보를 어떻게 저장할까.
#클래스로 선수들을 저장하고
#팀은 그 선수들의 리스트로 하면 어떨까.

#선수 정보는 이렇게 저장해주고 이거의 리스트를 클래스에 저장해두면 좋을듯.

import re
import pandas as pd

        
def player_info():
    con = input("정보를 알고자 하는 선수의 국가를 입력해주세요.")
    if (con == "대한민국") or (con == "대한민국")or(con =="한국") or (con =="우리나라") or (con =="우리 나라"):
        data = pd.read_csv('KOR_player.txt')
    elif (con == "일본" )or (con =="왜"):
        data = pd.read_csv('JPN_player.txt')
    elif (con == "오스트렐리아") or (con =="호주"):
        data = pd.read_csv('AUS_player.txt')
    elif (con == "우르과이") or (con =="우루과이"):
        data = pd.read_csv('URU_player.txt')
    elif con == "벨기에":
        data = pd.read_csv('BEL_player.txt')
    elif con == "브라질":
        data = pd.read_csv('BRA_player.txt')
    elif con == "캐나다":
        data = pd.read_csv('CAN_player.txt')
    elif con == "카메룬":
        data = pd.read_csv('CMR_player.txt')
    elif con == "크로아티아":
        data = pd.read_csv('CRO_player.txt')
    elif con == "코스타리카":
        data = pd.read_csv('CRC_player.txt')
    elif con == "에콰도르":
        data = pd.read_csv('ECU_player.txt')
    elif con == "잉글랜드":
        data = pd.read_csv('ENG_player.txt')
    elif con == "스페인":
        data = pd.read_csv('ESP_player.txt')
    elif con == "프랑스":
        data = pd.read_csv('FRA_player.txt')
    elif con == "독일":
        data = pd.read_csv('GER_player.txt')
    elif con == "가나":
        data = pd.read_csv('GHA_player.txt')
    elif con == "이란":
        data = pd.read_csv('IRN_player.txt')
    elif (con == "사우디라아비아") or (con =="사우디"):
        data = pd.read_csv('KSA_player.txt')
    elif con == "모로코":
        data = pd.read_csv('MAR_player.txt')
    elif con == "멕시코":
        data = pd.read_csv('MEX_player.txt')
    elif con == "네덜란드":
        data = pd.read_csv('NED_player.txt')
    elif con == "폴란드":
        data = pd.read_csv('POL_player.txt')
    elif (con == "포루투갈") or (con =="포르투갈"):
        data = pd.read_csv('POR_player.txt')
    elif con == "카타르":
        data = pd.read_csv('QAT_player.txt')
    elif con == "세네갈":
        data = pd.read_csv('SEN_player.txt')
    elif con == "스위스":
        data = pd.read_csv('SUI_player.txt')
    elif con == "세르비아":
        data = pd.read_csv('SRB_player.txt')
    elif con == "튀니지":
        data = pd.read_csv('TUN_player.txt')
    elif con == "아르헨티나":
        data = pd.read_csv('ARG_player.txt')
    elif con == "미국":
        data = pd.read_csv('USA_player.txt')
    elif con == "웨일스":
        data = pd.read_csv('WAL_player.txt')
    else:
        print("올바른 나라이름을 입력해주세요")

    para = input(" 선수 이름 혹은 등번호를 입력해주세요.")
    result = -1    
    if (any(temp. isdigit() for temp in para)):                                                                                             
        result = int(re.sub(r'[^0-9]', '', para))
    if result != -1:
        for i in range (26):
            if data.loc[i," 등 번호"] == result:
                print(data.loc[i])
                return
    else: 
        for i in range (26):
            if para in data.loc[i," 이름"]:
                print(data.loc[i])
                return
    print("정보를 올바르게 입력해주세요")
    return

def team_info():
        input_val = input("정보를 알고 싶은 국가의 이름을 입력해주세요.")
        data = pd.read_csv('team.txt')
        for i in range(32):
            if data.loc[i, "국가"] == input_val:
                print(input_val,'은 이번 월드컵', data.loc[i, " 소속 조"],'에 소속되어 있으며 피파 랭킹은' ,data.loc[i, " 피파 랭킹"],'입니다. 또한 이번 월드컵은', input_val,'의',data.loc[i, " 출전 횟수"], '입니다.' )
        return
team_info()
player_info()
                
                
                