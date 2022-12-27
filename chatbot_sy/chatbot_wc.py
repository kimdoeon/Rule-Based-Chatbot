# https://velog.io/@be1le/규칙-기반Rule-Based-챗봇-만들어-보기
import pandas as pd
import re
import requests
import json
import os
import math

idontknowstr="잘 알아듣지 못했어요~ 대한민국 화이팅!!!"

chatbot_data = pd.read_excel("chatbot_sy/chat_data.xlsx")# 파일 절대경로 필요
stadium_data = pd.read_excel('chatbot_sy/stadium_data.xlsx')# 파일 절대경로 필요
country = []
match_date = {}

def chatbot_init():
    
    query_weather = []
    query_stadium = []

    i = 0
    for data in chatbot_data['type']: # 날씨와 경기장에 관한 질문 데이터를 저장
        if data == '날씨':
            query_weather.append(chatbot_data['request'][i].split())
            i += 1
        
        elif data == '경기장':
            query_stadium.append(chatbot_data['request'][i].split()) 
            i += 1
    
    i = 0
    for ctry in stadium_data['country']:
        country.append(ctry)
        
    query_weather = set(sum(query_weather, [])) # 중복 제거
    query_stadium = set(sum(query_stadium, []))
    
    return query_weather, query_stadium

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
query_weather, query_stadium = chatbot_init()
#경기장 정보들
stadiums=[
    '1. 칼리파 국제 경기장\n칼리파 인터내셔널은 카타르에서 새로 건설되지 않은 유일한 카타르 축구 월드컵 경기장으로 카타르에서 가장 상징적인 경기장이며 실제로 1976년에 건설되었어요. 현지 기준에 따르면 구식에 가깝죠. 대규모 리노베이션을 마친 후 40,000석 규모로 2017년에 다시 개장하여 8강전까지 사용될 예정이에요. 선수와 팬 모두를 위한 이상적인 온도로 유지하는 고급 냉방 기술과 함께 상징적인 이중 아치 외부 구조가 이 스타디움의 근대성을 잘 보여줘요.\n칼리파 국제 경기장은 2022년 월드컵에서 팬들을 위한 주요 센터 역할을 할 기술 개발 및 혁신 지구인 도하의 어스파이어 존의 중심에 위치하고 있어요.\n주소: Al Waab St, Doha, Qatar',
    '2. 알 베이트 스타디움\n알 베이트 스타디움은 알 코르 시에 위치하고 있으며 2022년 월드컵 4강전이 이곳에서 열릴 예정이에요. 이 경기장은 수 세기 동안 아랍 세계에 거주하는 유목민인 베두인족이 사용하는 텐트를 나타내는 인상적인 디자인이 특징이에요.\n60,000석 규모의 스타디움은 쇼핑몰, 병원 등의 다양한 편의 시설을 갖춘 더 넓은 단지 내에 설치될 예정이에요. 도하에서 60km 떨어져 있어 가기 가장 어려운 곳 중 하나예요. 이곳을 여행하려면 택시나 버스를 이용하는 것이 가장 좋아요.\n주소: Al-Khor, Qatar',
    '3. 알 자누브 스타디움\n알 자누브 스타디움은 약 40,000석 규모의 정말 인상적인 경기장이에요. 세계적으로 유명한 건축가인 자하 하디드가 그녀 고유의 곡선 스타일로 설계한 이 세련된 카타르 스타디움은 아라비아 반도에서 오랫동안 운영되어 온 진주 채취 배의 선체에서 영감을 받았어요. 바로 이러한 이유로 경기장 건설에 전통적인 재료와 목재가 사용되었어요.\n알 자누브 스타디움은 알 와크라 시에 있어요. 도하에서 불과 20km 거리에 있어 전용 지하철 노선을 이용하면 알 와크라 시에 갈 수 있어요.\n주소: Al-Wakrah, Qatar',
    '4. 에듀케이션 시티 스타디움\n에듀케이션 시티 스타디움은 40,000석 규모의 경기장으로, 2022년 카타르 월드컵 8강전까지 열릴 계획이에요. 이 스타디움의 이름은 카타르의 주요 대학 캠퍼스에서 따온 거예요. 아직 완성되지 않았지만 그라운드는 낮에는 반짝거리고 밤에는 빛을 내는 톱니 모양의 다이아몬드 형태로 설계되었어요. 토너먼트 후 스타디움 규모를 반으로 줄여서 개도국에 경기장 건설을 위해 20,000석 이상을 기부할 예정이에요.\n에듀케이션 시티 스타디움은 도하 시내에서 단 7km 거리에 있어 차량이나 지하철로 쉽게 갈 수 있어요. 전체 지역은 녹지, 골프 코스, 최신 쇼핑몰로 가득해요.\n주소: Doha, Qatar' ,
    '5. 알 라얀 스타디움\n구 아메드 빈 알리 스타디움 부지에 위치한 알 라얀 스타디움은 카타르 월드컵 8강전까지 치룰 수 있는 규모로 40,000석이 넘어요.\n카타르에서 가장 전통적이고 유서 깊은 도시 중 하나인 알 라얀은 사막 끝에 위치하고 있으며 이곳에서 카타르의 깊은 문화적 뿌리를 엿볼 수 있어요. 도하에서 불과 몇 킬로미터 거리에 있어 전용 지하철 노선을 이용하면 갈 수 있어요.\n주소: Al Rayyan, Qatar',
    '6. 알 쑤마마 스타디움\n도하 중심부에서 12km 떨어진 곳에 위치한 40,000석 규모의 알 쑤마마 경기장은 현재 건설 중이에요. 이 경기장의 흥미로운 디자인은 아랍 남성들이 쓰는 전통 직조 모자인 가흐피야에서 영감을 얻었어요.\n2022년 월드컵의 많은 경기장과 마찬가지로 알 쑤마마도 토너먼트 후 규모를 반으로 줄여서 개발 도상국의 축구 및 스타디아 발전을 위해 20,000석 이상을 기부할 예정이에요. 이 스타디움은 도하에서 전용 지하철 노선으로 연결돼요.\n주소: Doha, Qatar',
    '7. 라스 아부 아부드 스타디움\n지속 가능성을 실현한 40,000석 규모의 라스 아부 아부드 스타디움은 만의 바닷가에 위치해 있으며 몇 킬로미터 떨어진 도하를 내려다보고 있어요. 운송 컨테이너와 기타 재활용품으로 만든 이 스타디움은 2022년 월드컵이 끝나면 철거되어 전국의 다른 건축 프로젝트에 사용될 예정이에요.\n이 경기장의 멋진 해안은 팬들에게 청량제 역할을 할 거예요. 만 바로 건너편에 있는 도하 시내에서 지하철을 타면 라스 아부 아부드에 금방 올 수 있어요.\n주소: Doha, Qatar',
    '8. 루사일 아이코닉 스타디움\n루사일 아이코닉 스타디움에서 2022년 월드컵 개막전과 결승전이 열릴 예정이에요. 현재 건설 중인 이 경기장은 86,000석이 넘는 규모이며 영국 건축가인 포스터 앤드 파트너스가 설계했어요. 고대 아랍 사발 직조 기술을 반영한 구조로 스타디움은 토너먼트의 개막 및 폐막을 위한 멋진 장소를 할 거예요\n경기장은 도하 북쪽에 위치한 계획 도시인 루사일 시티에 있어요. 놀랍게도 이번 행사를 위해 도시 전체가 특별히 건설되고 있어요. 월드컵이 시작될 때까지 루사일은 마리나, 아일랜드 리조트, 고급 쇼핑 및 레저 시설을 포함한 다양한 시설을 갖출 예정이에요. 도하 중심부에서 북쪽으로 15km 떨어진 루사일 아이코닉 스타디움은 수도에서 직행 지하철로 연결되어 쉽게 갈 수 있어요.\n주소: Lusail, Qatar',
]
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def chatbot(query):
    query = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", query) # 특수문자 제거
    
    match_weather = 0
    match_stadium = 0
    query_word = []
    
    for word in query.split(): # 질문이 날씨와 경기장 중 어느 쪽에 가까운지 분류
        query_word.append(word)
        
        if word in query_weather:
            match_weather += 1
            
        if word in query_stadium:
            match_stadium += 1
            
    ask_type = ['날씨', '경기장']
    
    if match_weather == match_stadium == 0:
        return idontknowstr
    if match_weather == 1 and '정보' in query:
        return idontknowstr
    if match_stadium == 1 and '정보' in query:
        return idontknowstr
    if match_weather > match_stadium:
        return chat_flow(ask_type[0], '') #날씨
    
    if match_weather <= match_stadium:
        for word in query_word:
            for i in range(len(country)):
                if word in country[i]:
                    # print("country :", word)
                    return chat_flow(ask_type[1], country[i])
        return chat_flow(ask_type[1], '') #경기장

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+    

def chat_flow(flow, ctry):         # 질문에 대한 답
    rtstring = []
    match_place = []
    place_date = []
    
    if flow == '날씨':
        return weather_info()
    
    elif flow == '경기장':
        if ctry == '':
            rtstring.append("카타르 월드컵 경기장 정보입니다.\n")
            for st in stadiums:
                rtstring.append("--------------------------------------\n")
                rtstring.append(st)
                rtstring.append("\n")
            rtstring.append("--------------------------------------\n")
            return rtstring
        else:
            idx = country.index(ctry)
            # print("idx = ", idx)
            # print(stadium_data['country'][idx])
            # print(stadium_data.columns[1:])
            # print("printing test: ", stadium_data[stadium_data.columns[2]][idx])
            tmp_var = 0
            for i in stadium_data.columns[1:]:
                if stadium_data[i][idx] != '':
                    # print("printing test2 : ", stadium_data[i][idx])

                    match_date[tmp_var] = stadium_data[i][idx]
                    # print("\t<< DEBUG >>")
                    # print("match info :",match_date)
                tmp_var += 1
            # print("What is type of nan? :", type(match_date[0]))
            
            for i in range(len(match_date)):
                # print("match_DATE:", match_date[i])
                
                if type(match_date[i]) == type(0.001) :
                    # print("nan")
                    continue
                
                elif type(match_date[i]) == type('a'):   
                    # print("list num")
                    cng_int = list(map(int, match_date[i].split()))
                    match_place.append(stadiums[i])

                    place_date.append(cng_int)
                
                else:
                    # print("int")
                    match_place.append(stadiums[i])
                    if match_date[i] > 0:
                        place_date.append(match_date[i])
                    # place_date.append(match_date[i])
            # print("Place DATE: ", place_date)
            if idx == 2 or idx == 17:
                nara = country[idx].split()[0]
                strings = f"{nara} 이(가) 경기하는 곳은\n"
            else:
                strings = f"{country[idx]}이(가) 경기하는 곳은\n"
            rtstring.append(strings)
            
            for i in range(len(match_place)):
                # print("last check: ", place_date[i])
                if type(place_date[i]) == type([1]):
                    for date in place_date[i]:
                        if date >= 20:
                            rtstring.append("11월" + str(date))
                        else:
                            rtstring.append("12월" + str(date))       
                                             
                elif place_date[i] >= 20:
                    rtstring.append("11월" + str(place_date[i]))
                else:
                    rtstring.append("12월" + str(place_date[i]))
                rtstring.append(match_place[i])
                rtstring.append("\n")

    return rtstring

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def weather_info():
    api = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid=51a148054b5199e5e2ee3d7ef56046b9"

    k2c = lambda k : k - 273.15 #절대온도 -> 섭씨온도

    cities = "Doha"
    url = api.format(city = cities)
    r = requests.get(url)
    data = json.loads(r.text)

    city_name = data['name']
    weather = data["weather"][0]["description"]
    tmp_max = round(k2c(data["main"]["temp_max"]))
    tmp_min = round(k2c(data["main"]["temp_min"]))
    humid = data["main"]["humidity"]

    rtstring = []
    rtstring.append("--------------------------------------")
    rtstring.append(f"| 도시 :\t {city_name}")
    rtstring.append(f"| 날씨 :\t {weather}")
    rtstring.append(f"| 최고 기온 :\t {tmp_max}도") # 이거... 당일 최고/최저가 아니라 그 순간꺼 인거 같음
    rtstring.append(f"| 최저 기온 :\t {tmp_min}도") # 그냥 더운 나라 점심때라 둘 다 높은거였네......
    rtstring.append(f"| 습도 :\t {humid}%")
    rtstring.append("--------------------------------------")
    return rtstring
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

if __name__ == "__main__":
    print('안녕하세요. 카타르 현지 날씨와 경기장 정보를 알려드리는 챗봇입니다.')
    while True:
        query = input('채팅을 입력하세요(종료: q, ㅂ): ')
        
        if query == 'q' or query == 'ㅂ':
            break
        
        else:
            chatbot(query)