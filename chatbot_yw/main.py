import pandas as pd
import re
PLlist =['./chatbot_yw/KOR_player.txt',
         './chatbot_yw/JPN_player.txt',
         './chatbot_yw/AUS_player.txt',
         './chatbot_yw/URU_player.txt',
         './chatbot_yw/BEL_player.txt',
         './chatbot_yw/BRA_player.txt',
         './chatbot_yw/CAN_player.txt',
         './chatbot_yw/CMR_player.txt',
         './chatbot_yw/DEN_player.txt',
         './chatbot_yw/CRO_player.txt',
         './chatbot_yw/CRC_player.txt',
         './chatbot_yw/ECU_player.txt',
         './chatbot_yw/ENG_player.txt',
         './chatbot_yw/ESP_player.txt',
         './chatbot_yw/FRA_player.txt',
         './chatbot_yw/GER_player.txt',
         './chatbot_yw/GHA_player.txt',
         './chatbot_yw/IRN_player.txt',
         './chatbot_yw/KSA_player.txt',
         './chatbot_yw/MAR_player.txt',
         './chatbot_yw/MEX_player.txt',
         './chatbot_yw/NED_player.txt',
         './chatbot_yw/POL_player.txt',
         './chatbot_yw/POR_player.txt',
         './chatbot_yw/QAT_player.txt',
         './chatbot_yw/SEN_player.txt',
         './chatbot_yw/SUI_player.txt',
         './chatbot_yw/SRB_player.txt',
         './chatbot_yw/TUN_player.txt',
         './chatbot_yw/ARG_player.txt',
         './chatbot_yw/USA_player.txt',
         './chatbot_yw/WAL_player.txt'
         ]
GK = ["골키퍼" ,'골 키퍼' , 'GK' ,"goal keeper" , 'goalkeeper' , "Goal keeper" , 'Goalkeeper', "Goal Keeper" ,'GoalKeeper']
FW = ["공격수", '공격', '스트라이커', 'FW', 'Forward', 'fw','Fw',"forward"]
DF = ['수비수', '수비', 'DF', "defend",'Defencer','defencer', 'Defend']
MF = ['미드필더', 'MF', 'Mf','Mid fielder','Midfielder','Mid Fielder','MidFielder','mid fielder','midfielder']

idontknowstr="잘 알아듣지 못했어요~ 대한민국 화이팅!!!"

def team_info_2(user_input:'str'):
    msg = ""
    data = pd.read_csv('./chatbot_yw/team.txt')
    for i in range(32):
        if(data.loc[i , '국가'] in user_input):
            #print(data.loc[i])
            # print(data.loc[i , '국가'],' 국가는 이번 월드컵', data.loc[i, " 소속 조"],'에 소속되어 있으며 피파 랭킹은' ,data.loc[i, " 피파 랭킹"],' 입니다. 또한 이번 월드컵은 ', data.loc[i , '국가'],'의',data.loc[i, " 출전 횟수"], '입니다.',sep = "" )
            msg+=f" {data.loc[i , '국가']} 국가는 이번 월드컵 {data.loc[i, ' 소속 조']}에 소속되어 있으며 피파 랭킹은 {data.loc[i, ' 피파 랭킹']} 입니다. 또한 이번 월드컵은 {data.loc[i , '국가']}의 {data.loc[i, ' 출전 횟수']}입니다."
    return msg

def player_info2(user_input):
    msg = ""
    for i in PLlist:
        data = pd.read_csv(i)
        #print(data.get(0))
        #print(i)
        #print(data)
        국가 = 0
        if i =='./chatbot_yw/KOR_player.txt':
            국가 = "대한민국"
        elif i =='./chatbot_yw/JPN_player.txt':
            국가 = '일본'
        elif i =='./chatbot_yw/AUS_player.txt':
            국가 = '호주'
        elif i =='./chatbot_yw/URU_player.txt':
                국가 = '우르과이'
        elif i =='./chatbot_yw/BEL_player.txt':
            국가 = '벨기에'
        elif i =='./chatbot_yw/BRA_player.txt':
            국가 = '브라질'
        elif i =='./chatbot_yw/CAN_player.txt':
            국가 = '캐나다'
        elif i =='./chatbot_yw/CMR_player.txt':
            국가 = '카메룬'
        elif i =='./chatbot_yw/DEN_player.txt':
            국가 = '덴마크'
        elif i =='./chatbot_yw/CRO_player.txt':
            국가 = '크로아티아'
        elif i =='./chatbot_yw/CRC_player.txt':
            국가 = '코스타리카'
        elif i =='./chatbot_yw/ECU_player.txt':
            국가 = '에콰도르'
        elif i =='./chatbot_yw/ENG_player.txt':
            국가 = '잉글랜드'
        elif i =='./chatbot_yw/ESP_player.txt':
            국가 = '스페인'
        elif i =='./chatbot_yw/FRA_player.txt':
            국가 = '프랑스'
        elif i =='./chatbot_yw/GER_player.txt':
            국가 = '독일'
        elif i =='./chatbot_yw/GHA_player.txt':
            국가 = '가나'
        elif i =='./chatbot_yw/IRN_player.txt':
            국가 = '이란'
        elif i =='./chatbot_yw/KSA_player.txt':
            국가 = '사우디 아라비아'
        elif i =='./chatbot_yw/MAR_player.txt':
            국가 = '모로코'
        elif i =='./chatbot_yw/MEX_player.txt':
            국가 = '멕시코'
        elif i =='./chatbot_yw/NED_player.txt':
            국가 = '네덜란드'
        elif i =='./chatbot_yw/POL_player.txt':
            국가 = '폴란드'
        elif i =='./chatbot_yw/POR_player.txt':
            국가 = '포루투갈'
        elif i =='./chatbot_yw/QAT_player.txt':
            국가 = '카타르'
        elif i =='./chatbot_yw/SEN_player.txt':
            국가 = '세네갈'
        elif i =='./chatbot_yw/SRB_player.txt':
            국가 = '세르비아'
        elif i =='./chatbot_yw/SUI_player.txt':
            국가 = '스위스'
        elif i =='./chatbot_yw/TUN_player.txt':
            국가 = '튀니지'
        elif i =='./chatbot_yw/ARG_player.txt':
            국가 = '아르헨티나'
        elif i =='./chatbot_yw/USA_player.txt':
            국가 = '미국'
        elif i =='./chatbot_yw/WAL_player.txt':
            국가 = '웨일스'
        for j in range(len(data)):
            if (user_input in data.loc[j, ' 이름']) or (data.loc[j, ' 이름'] in user_input ):
                # print(data.loc[j, ' 이름']," 선수는 ", 국가,"팀의 ", data.loc[j, ' 등 번호'],'번 선수입니다. ','포지션은 ',data.loc[j, '포지션'],'이며 ', data.loc[j, ' 생년월일'],'생으로', data.loc[j, ' 나이'],'입니다. 국가 대표 경기 출전 횟수는 ',data.loc[j, ' 국가대표 경기 출전 횟수'],'번 이며 ',data.loc[j, ' 골 수'],'골을 기록하였으며 현재 소속팀은 ',data.loc[j, ' 현재 소속 팀'],'입니다.' ,sep = '')
                msg+=f"{data.loc[j, ' 이름']} 선수는 {국가} 팀의 { data.loc[j, ' 등 번호']}번 선수입니다. 포지션은 {data.loc[j, '포지션']}이며 {data.loc[j, ' 생년월일']}생으로 {data.loc[j, ' 나이']}입니다. 국가 대표 경기 출전 횟수는 {data.loc[j, ' 국가대표 경기 출전 횟수']}번 이며 {data.loc[j, ' 골 수']}골을 기록하였으며 현재 소속팀은 {data.loc[j, ' 현재 소속 팀']}입니다."
                return msg
    return 0
def team_checker(con):
    data = -1
    if ("대한민국" in con) or ("대한 민국" in con)or("한국" in con) or ("우리나라" in con) or ("우리 나라" in con):
        data = pd.read_csv('./chatbot_yw/KOR_player.txt')
        국가 = '대한민국'
    elif ("일본" in con)or ("왜" in con):
        data = pd.read_csv('./chatbot_yw/JPN_player.txt')
        국가 = '일본'
    elif ("오스트렐리아" in con) or ("호주" in con):
        data = pd.read_csv('./chatbot_yw/AUS_player.txt')
        국가 = '호주'
    elif ("우르과이" in con) or ("우루과이" in con):
        data = pd.read_csv('./chatbot_yw/URU_player.txt')
        국가 = '우르과이'
    elif  "벨기에" in con:
        data = pd.read_csv('./chatbot_yw/BEL_player.txt')
        국가 = '벨기에'
    elif  "브라질" in con:
        data = pd.read_csv('./chatbot_yw/BRA_player.txt')
        국가 = '브라질'
    elif "캐나다" in con:
        data = pd.read_csv('./chatbot_yw/CAN_player.txt')
        국가 = '캐나다'
    elif "카메룬" in con:
        data = pd.read_csv('./chatbot_yw/CMR_player.txt')
        국가 = '카메룬'
    elif "크로아티아" in con:
        data = pd.read_csv('./chatbot_yw/CRO_player.txt')
        국가 = '크로아티아'
    elif "코스타리카" in con:
        data = pd.read_csv('./chatbot_yw/CRC_player.txt')
        국가 = '코스타리카'
    elif "에콰도르" in con:
        data = pd.read_csv('./chatbot_yw/ECU_player.txt')
        국가 = "에콰도르"
    elif  "잉글랜드" in con:
        data = pd.read_csv('./chatbot_yw/ENG_player.txt')
        국가 = '잉글랜드'
    elif"스페인" in con:
        data = pd.read_csv('./chatbot_yw/ESP_player.txt')
        국가 = '스페인'
    elif  "프랑스" in con:
        data = pd.read_csv('./chatbot_yw/FRA_player.txt')
        국가 = "프랑스"
    elif "독일" in con:
        data = pd.read_csv('./chatbot_yw/GER_player.txt')
        국가 = '독일'
    elif "가나" in con:
        data = pd.read_csv('./chatbot_yw/GHA_player.txt')
        국가 = '가나'
    elif "이란" in con:
        data = pd.read_csv('./chatbot_yw/IRN_player.txt')
        국가 = '이란'
    elif ("사우디라아비아" in con) or ("사우디" in con):
        data = pd.read_csv('./chatbot_yw/KSA_player.txt')
        국가 = '사우디 아라비아'
    elif "모로코" in con:
        data = pd.read_csv('./chatbot_yw/MAR_player.txt')
        국가 = '모로코'
    elif "멕시코" in con:
        data = pd.read_csv('./chatbot_yw/MEX_player.txt')
        국가 = '멕시코'
    elif "네덜란드" in con:
        data = pd.read_csv('./chatbot_yw/NED_player.txt')
        국가 = '네덜란드'
    elif  "폴란드" in con:
        data = pd.read_csv('./chatbot_yw/POL_player.txt')
        국가 = '폴란드'
    elif ( "포루투갈" in con) or ("포르투갈" in con):
        data = pd.read_csv('./chatbot_yw/POR_player.txt')
        국가 = '포루투갈'
    elif "카타르" in con:
        data = pd.read_csv('./chatbot_yw/QAT_player.txt')
        국가 = '카타르'
    elif "세네갈" in con:
        data = pd.read_csv('./chatbot_yw/SEN_player.txt')
        국가 = '세네갈'
    elif "스위스" in con:
        data = pd.read_csv('./chatbot_yw/SUI_player.txt')
        국가 = '스위스'
    elif "세르비아" in con:
        data = pd.read_csv('./chatbot_yw/SRB_player.txt')
        국가 = '세르비아'
    elif "튀니지" in con :
        data = pd.read_csv('./chatbot_yw/TUN_player.txt')
        국가 = '튀니지'
    elif "아르헨티나" in con:
        data = pd.read_csv('./chatbot_yw/ARG_player.txt')
        국가 ='아르헨티나'
    elif "미국"in con:
        data = pd.read_csv('./chatbot_yw/USA_player.txt')
        국가 ='미국'
    elif "웨일스" in con:
        data = pd.read_csv('./chatbot_yw/WAL_player.txt')
        국가 = '웨일스'
    else:
        국가 = None
    
    return data , 국가

def position_checker(user_input):
    for i in GK:
        if i in user_input:
            return 'GK'
    for i in FW:
        if i in user_input:
            return 'FW'
    for i in DF:
        if i in user_input:
            return 'DF'
    for i in MF:
        if i in user_input:
            return 'MF'
        
    return 0

def player_team_all(user_input):
    msg = []
    #1. 만약 이름이 있으면 해당 이름을 출력해준다.
    player = 0
    player = player_info2(user_input)
    #2.나라 이름이 들어있는지 확인한다.
    #print(player)
    if player:
        msg.append(player)
        return msg
    else:
        data = 0 
        data, 국가 = team_checker(user_input)
        #print(data)
        #만약 나라 이름 있다면?
        #print(1)
        #print(type(data))
        if  str(type(data) )== "<class 'pandas.core.frame.DataFrame'>":
            #포지션을 확인한다.
            #print(1)
            pos = 0
            pos = position_checker(user_input)
            #만약 포지션이 있다면?
            tmp=[]
            if pos != 0:
                #추출 해둔 국가에서 해당 포지션을 가진 아이들을 모두 출력한다.
                # print(pos,'포지션을 가진',국가 ,'선수는', end =" ")
                msg.append( f"{pos}포지션을 가진 {국가} ,선수는 ")
                for i in range(len(data)):
                    if data.loc[i , '포지션'] == pos:
                        # print(data.loc[i,' 이름'],end = ', ')
                        msg.append( f"{data.loc[i,' 이름']}, ")
                # print("입니다.") 
                msg.append( "입니다.")
                return msg
            elif (any(temp.isdigit() for temp in user_input)):  
                #번호가 있다면 그 나라의 그 번호 선수 알려준다.                                                                                            
                num = int(re.sub(r'[^0-9]', '', user_input))
                for i in range (len(data)):
                    if data.loc[i," 등 번호"] == num:
                        msg.append( f"{국가}팀의 {data.loc[i, ' 등 번호']}번 선수는 {data.loc[i, ' 이름']} 입니다. 포지션은 {data.loc[i, '포지션']}이며 {data.loc[i, ' 생년월일']} 생으로 {data.loc[i, ' 나이']} 입니다. 국가 대표 경기 출전 횟수는 {data.loc[i, ' 국가대표 경기 출전 횟수']}번 이며 {data.loc[i, ' 골 수']}골을 기록하였으며 현재 소속팀은 {data.loc[i, ' 현재 소속 팀']}입니다.")
                        return msg
            elif ('선수' in user_input):
                msg.append(f"{data}")
                return msg
            else: 
                #나라 이름은 있는데 등번호도, 포지션도 없다면?
                
                msg.append(team_info_2(user_input))
                return msg
        else:
        #만약 나라 이름이 없는 상태라면?
            return idontknowstr            
            
if __name__ == "__main__":
    player_team_all("대한민국 공격수")