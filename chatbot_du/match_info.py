from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
from konlpy.tag import Okt
import re
import datetime


matchDataFile = pd.read_excel('./chatbot_du/matchInfo.xlsx')

idontknowstr="잘 알아듣지 못했어요~ 대한민국 화이팅!!!"

#엑셀에서 읽어온 경기정보 딕셔너리 형태로 변환
matches=[]
for i in range(0, len(matchDataFile)-1,2):
    tmp = {
    'date' :[],
    'time':[],
    'group':[],
    'country':[],
    'status':[],    
    'score' :[],
    'record' :[],
    }	
    tmp['date'].append(matchDataFile['date'][i])
    tmp['time'].append(matchDataFile['time'][i])
    tmp['group'].append(matchDataFile['group'][i])
    tmp['country'].append(matchDataFile['country'][i])
    tmp['country'].append(matchDataFile['country'][i+1])
    tmp['status'] = matchDataFile['status'][i]
    tmp['score'] = matchDataFile['score'][i]
    tmp['record'].append(matchDataFile['record'][i])
    tmp['record'].append(matchDataFile['record'][i+1])
    
    matches.append(tmp)

#룰 읽어오기
rules = pd.read_excel("./chatbot_du/rule.xlsx")

#형태소 분석 
okt=Okt()

'''
print("===============================================================================")
print("제공 정보 : 경기 날짜 및 시간/ 경기 조 / 경기 상태 /나라 / 경기 결과 /나라별 전적")
print("※ 나라, 날짜, 조 중 하나는 필수 입력 사항입니다 ※")
print("정확한 경기 정보를 얻기 위해 위를 참고하여 다음과 같이 작성해 주세요.")
print("===============================================================================")
print("예) 11월 30일 경기 정보 알려줘")
print("예) 대한민국 경기 날짜,시간 알려줘")
print("예) H조 정보 알려줘")
print("예) 대한민국 오늘 경기 결과 알려줘")
print("===============================================================================")
'''

# 경기 정보 크롤링 함수
def crawling_match_info():
  driver = wd.Chrome('C:\chromedriver') # 크롬드라이버 경로
  driver.maximize_window() # 크롬창 크기 최대

  url = "https://m.sports.naver.com/qatar2022/schedule/index"

  driver.get(url)
  html = driver.page_source 
  soup = BeautifulSoup(html, 'lxml')

  #크롤링한 경기 정보를 엑셀로 저장하기 위한 딕셔너리
  data = {
    'date' :[],
    'time':[],
    'group':[],
    'country':[],
    'status':[],    
    'score' :[],
    'record' :[],
  }

  #날짜별 경기 정보
  allLeagues = [match for match in soup.find_all('div', attrs={'class':'game_box_list'})]

  #조별 경기 정보 저장 리스트
  matchInfos=[]

  for league in allLeagues:
    matches = [match for match in league.find_all("div",attrs={"class":"ScheduleGameBox_game_box__23m0b"})]
    for match in matches:
      matchInfos.append(match)

  #조별 경기 정보 추출
  for matchInfo in matchInfos:

    # 조 <em class="ScheduleGameBox_game_info__2Iapg">조별리그 A조</em>
    group  = (matchInfo.find("em",attrs={'class':'ScheduleGameBox_game_info__2Iapg'})).get_text()
    data['group'].extend([group,group])

    #나라 <strong class="ScheduleGameBox_name__3QDbf">네덜란드</strong>
    for c in [countries for countries in matchInfo.find_all("strong",attrs={'class':'ScheduleGameBox_name__3QDbf'})]:
      country = c.get_text()
      data['country'].append(country)

    #날짜, 시간 정보 <span class="ScheduleGameBox_text__2RCBe">경기종료</span>
    dateAndTimes = (matchInfo.find("em",attrs={'class':'ScheduleGameBox_status__LQyL-'})).get_text()
    
    #경기상태 <span class="ScheduleGameBox_text__2RCBe">경기종료</span>
    status = (matchInfo.find("span",attrs={'class':'ScheduleGameBox_text__2RCBe'})).get_text()
    data['status'].extend([status,status])

    #경기 종료시 날짜/시간 정보 추출
    if status=="경기종료":
      dateAndTimes = dateAndTimes[11:]
    #경기전 날짜/시간 정보 추출
    else:  
      dateAndTimes = dateAndTimes[10:]
    
    #날짜
    date = (dateAndTimes.split(" "))[0]
    data['date'].extend([date,date])
    #시간
    time = (dateAndTimes.split(" "))[1]
    data['time'].extend([time,time])
    
    #경기 결과 <span class="ScheduleGameBox_number__3T3_C">0</span>
    if status=="경기종료":
      scoreInfo = [score.get_text() for score in matchInfo.find_all("span",attrs={'class':'ScheduleGameBox_number__3T3_C'})]
      score = " : ".join(scoreInfo)
      data['score'].extend([score,score])
    else:
      score = "미정"
      data['score'].extend([score,score])

    #전적 <em class="ScheduleGameBox_record__2Xccw">0승 0무 1패</em>
        #<div class="ScheduleGameBox_record__2Xccw">1승 0무 0패</div>
    for r in [record for record in matchInfo.find_all(attrs={"class": "ScheduleGameBox_record__2Xccw"})]:
      record = r.get_text()
      data['record'].append(record)

  #경기정보 데이터프레임 생성
  dataFrame = pd.DataFrame(data)
  #경기정보 데이터프레임 엑셀로 저장
  dataFrame.to_excel('./chatbot_du/matchInfo.xlsx')

#user input 분석 함수
#user input을 형태소 단위로 분석해
#user 요청의 정보와, 요청에 관한 경기 정보를 리턴한다.
GK = ["골키퍼" ,'골 키퍼' , 'GK' ,"goal keeper" , 'goalkeeper' , "Goal keeper" , 'Goalkeeper', "Goal Keeper" ,'GoalKeeper']
FW = ["공격수", '공격', '스트라이커', 'FW', 'Forward', 'fw','Fw',"forward"]
DF = ['수비수', '수비', 'DF', "defend",'Defencer','defencer', 'Defend']
MF = ['미드필더', 'MF', 'Mf','Mid fielder','Midfielder','Mid Fielder','MidFielder','mid fielder','midfielder']
def anal_user_input(userInput,matches,rules,okt):

  #rule 엑셀 파일을 각 규칙에 대한 리스트로 변환
  #<<경합집합>>
  rule1 = list(rules['rule1'])
  rule2 = list(rules['rule2'])
  intent1 = list(rules['intent1'])

  #user 요청 정보 저장 딕셔너리
  request = {
    'date' :[],
    'time':[],
    'group':[],
    'country':[],
    'status':[],    
    'score' :[],
    'record' :[],
  }

  #user input 형태소 단위로 쪼개기
  nouns = okt.morphs(userInput)

  #input 문장 분석(request에 user 요청 분류해 저장)-----------------------------------
  #<<경합 해소>>

  #실제 날짜 정보 저장 리스트
  date=[]

  #조 판별을 위한 인덱스
  groupIdx=0

  for noun in nouns:
    
    if noun in ['날씨','경기장','선수','팀','번호','포지션']:
      return [],[]

    elif noun in GK:
      return [],[]

    elif noun in FW:
      return [],[]

    elif noun in DF:
      return [],[]

    elif noun in MF:
      return [],[]

    # 실제 정보가 없는 요청일 경우 (예)언제, 몇시, 누구, 나라, 몇대몇 ...
    elif noun in rule1:
      idx = rule1.index(noun)
      intent = intent1[idx]
      request[intent[2:]].append(intent)
    
    #실제 정보 처리
    # 나라 처리
    elif noun in rule2:
      request['country'].append(noun)
 
    #날짜 처리
    elif re.search(r'\d', noun) and (noun[-1]=='월' or noun[-1]=='일'):
      date.append("".join(re.findall('\d', noun)))
    #날짜로 변환
    elif noun in ["오늘","내일","모레","어제"]:
      dt_now = datetime.datetime.now()
      if noun == "오늘":
        dt_month = dt_now.month
        dt_day = dt_now.day
      elif noun == "내일":
        dt_month = dt_now.month
        dt_day = dt_now.day+1
      elif noun == "모레":
        dt_month = dt_now.month
        dt_day = dt_now.day+2
      elif noun == "어제":
        dt_month = dt_now.month
        dt_day = dt_now.day-1
      request['date'].append(str(dt_month) + "." + str(dt_day) + ".")
    
    #조 처리
    elif noun == "조":
      if nouns[groupIdx-1].encode().isalpha():
        request['group'].append(f"조별리그 {nouns[groupIdx-1].upper()}조")
      else:
        request['group'].append("q_group")
   
    #시간 처리
    elif re.search(r'\d', noun) and noun[-1]=='시':
      if(len(noun)==2):
        request['time'].append(f"0{noun[:1]}:00")
      elif((len(noun)==3)):
        request['time'].append(f"{noun[:2]}:00")
    groupIdx+=1

  #날짜 처리 
  if date:
    for i in range(0,len(date)-1,2):
      request['date'].append(date[i]+"."+date[i+1]+".")
  #---------------------------------------------------------------------------------------------------
  
  filterLIst = []
 

  # 나라, 조, 시간 추출
  for key,val in request.items():
    if  val and val[0][:2] !="q_":
      if filterLIst:
        tmp = []
        for match in filterLIst:
          if [k for k in match[key] if k in val]:
            tmp.append(match)
        filterLIst = tmp
      else:
        for match in matches:
          if [c for c in match[key] if c in val]:
            filterLIst.append(match)

  return request,filterLIst

def chatbot(userInput):
  
  if userInput == 'q' or userInput == 'Q' or userInput == 'ㅂ' :
    print(">>대화를 종료합니다.")
    return 0

  else:
    userReq, response = anal_user_input(userInput,matches,rules,okt)

    if not response or not userReq:
      return idontknowstr

    else:
      qres_list=[]
      res_list=[]

      #qres res분류
      for key,value in userReq.items():
        if [v for v in value if v[:2] == "q_"]:
          for v in value:
            if v and v[:2] == "q_":
              qres_list.append(v[2:])
        elif value:
          res_list.append(key)     

      if qres_list:
        msg = []
        for q in qres_list:
          if userReq['country'] and q!='country':
            for c in userReq['country']:
                for match in response:
                  if c in match['country']:
                    #기록 질문일 경우
                    if q == "record":
                      idx = match['country'].index(c)
                      return(f">>{c} 전적: {match['record'][idx]}")
                    #날짜/시간 질문일 경우
                    elif q == "date" or q == "time":
                      msg.append(f">>{c}: {match['date']}일 {match['time']}시")
                    #경기 결과 질문일 경우
                    elif q == "score":
                      msg.append(f">>{c}: {match['date']}일, {match['country'][0]} vs {match['country'][1]} : {match['score']}")
                    #조 질문일 경우
                    elif q == "group":
                      return(f">>{c}: {match['group']}")
                      break
                    #상태 질문일 경우
                    elif q == "status":
                      msg.append(f">>{c}: {match['date']}일, {match['country'][0]} vs {match['country'][1]} : {match['status']}")
            return msg

          else:
            msg = []
            for match in response:
              #날짜/시간 질문일 경우
              if q == "date" or q == "time":
                msg.append(f">>{match['date']}일 {match['time']}시")
              #경기 결과 질문일 경우
              elif q == "score":
                msg.append(f">>{match['date']}일, {match['country'][0]} vs {match['country'][1]} : {match['score']}")
              #조 질문일 경우
              elif q == "group":
                msg.append(f">>{response[i]['date']}일, {response[i]['group']}의 경기가 있습니다.")
              #상태 질문일 경우
              elif q == "status":
                msg.append(f">>{match['date']}일, {match['country'][0]} vs {match['country'][1]} : {match['status']}")
              #나라 질문일 경우
              elif q == "country":
                if userReq['group']:
                    country_list=[]
                    for match in response:
                      country_list.extend([c for c in match['country'] if c not in country_list])
                      msg = " ".join(country_list)
                    return(f">>{msg}가 있습니다.")
                    break
                else:
                  msg.append(f">>{match['date']}일 {match['country'][0]} 와/과 {match['country'][1]}의 경기가 있습니다.") 
            return msg

      else:
        msg=[]
        for match in response:
          msg.append(f"<{match['date'][0]}일 {match['time'][0]}시, {match['group'][0]} 경기 정보>")
          msg.append(f"{match['country'][0]} vs {match['country'][1]} : {match['score']}")
          msg.append(f"{match['country'][0]} 전적 :  {match['record'][0]}.")
          msg.append(f"{match['country'][1]} 전적 :  {match['record'][1]}.")
        return msg     
  return

#챗봇 함수
if __name__ == "__main__":
  print("===============================================================================")
  print("제공 정보 : 경기 날짜 및 시간/ 경기 조 / 경기 상태 /나라 / 경기 결과 /나라별 전적")
  print("※ 나라, 날짜, 조 중 하나는 필수 입력 사항입니다 ※")
  print("정확한 경기 정보를 얻기 위해 위를 참고하여 다음과 같이 작성해 주세요.")
  print("===============================================================================")
  print("예) 11월 30일 경기 정보 알려줘")
  print("예) 대한민국 경기 날짜,시간 알려줘")
  print("예) H조 정보 알려줘")
  print("예) 대한민국 오늘 경기 결과 알려줘")
  print("===============================================================================")
  # crawling_match_info()
  # while(1):
  #   input_str = input()
  #   chatbot(input_str)
