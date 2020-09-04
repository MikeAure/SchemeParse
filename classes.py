from bs4 import BeautifulSoup
import requests
from parse import initInfo
import lxml
import json
import re
class Class:
    def __init__(self,**kwargs):
        self.className=kwargs['name']
        self.location=kwargs['loc']
        self.teacherName=kwargs['teacherName']
        self.goal=kwargs['goal']
        self.totalNum=kwargs['totalNum']

allClasses={}
# totalWeeks=input("Please input your total week number:")
# num=int()
# week=[{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''}]
# for i in range(int(totalWeeks)):
#     num=i+1
#     allClasses.update({num:week})

# url="http://202.115.133.173:805/Classroom/ProductionSchedule/StuProductionSchedule.aspx"
# header={'Cookie': 'ASP.NET_SessionId=v4x03ubilwsodb3ojpufvcfl; UserTokeID=d1c08ee9-6fb2-4c98-9f4c-2053e36c34d8'}
# info={'termid':'202001','stuID':'201917030119'}
# htmli=requests.get(url=url,params=info,headers=header)
# rs=htmli.text
#
# with open("result.html","w",encoding="utf-8") as f:
#     f.write(rs)


soup=BeautifulSoup(open("./StuProductionSchedule.htm",encoding="utf-8"),"html.parser")
soup.prettify()
# with open("result.html","w",encoding="utf-8") as f:
#     f.write(str(soup))
rs=soup.find_all("tr")
for i in range(4):
    del rs[0]

def login(Cookie:str,termid:str,stuID:str):
    url="http://202.115.133.173:805/Classroom/ProductionSchedule/StuProductionSchedule.aspx"
    header={'Cookie': Cookie}
    info={'termid':termid,'stuID':stuID}
    htmli=requests.get(url=url,params=info,headers=header)
    rs=htmli.text
    with open("result.html","w",encoding="utf-8") as f:
        f.write(rs)
    return f

def judge(weekdayCal,oneday,weekdayTemp,classContent,weekday,currentWeek):
    if weekdayCal == 2:
        oneday.update({"1-2": classContent})
    elif weekdayCal == 4:
        oneday.update({"3-4": classContent})
    elif weekdayCal == 7:
        oneday.update({"5-6": classContent})
    elif weekdayCal == 9:
        oneday.update({"7-8": classContent})
    elif (weekdayCal == 11 and classContent!='')or weekdayCal==12:
        oneday.update({"9-11": classContent})
        currentWeek.append({weekday: oneday.copy()})
        if weekday <= 7:
            weekday += 1
            weekdayCal = 0
        oneday.clear()
        return (weekdayCal,weekday)

    return (weekdayCal,weekday)


# print(rs[0].contents)
def parseScheme(rs):
    wholeClasses={}
    print(type(rs[0].contents))
    for tr in rs:
        lr=tr.find_all('td')#tr块中所有td标签
        oneday={}
        currentWeek=[]
        weekday=1
        weekdayCal=0
        for tdItem in lr:
            if tdItem["class"]==['td1']:
                weekNum=int(next(tdItem.stripped_strings)[0:-1])
                wholeClasses.update({weekNum:[]})
                continue

            if tdItem["class"] == ["fontcss"]:
                if tdItem.has_attr("colspan") and tdItem["colspan"]=='12':
                    weekday+=1
                    continue
                else:
                    if tdItem.has_attr("colspan"):
                        weekdayTemp=int(tdItem["colspan"])
                    else:
                        weekdayTemp=1
                    classContent=str()
                    for content in tdItem.stripped_strings:
                        classContent=classContent+content+' '
                    weekdayCal+=weekdayTemp
                    (weekdayCal,weekday)=judge(weekdayCal,oneday,weekdayTemp,classContent,weekday,currentWeek)

        wholeClasses[weekNum]=currentWeek
    toJson = json.dumps(wholeClasses, ensure_ascii=False)
    with open("jsonrs.json", "w", encoding="utf-8")as f:
        f.write(toJson)

    return wholeClasses


def classInfoGet(rs:BeautifulSoup):
    rs.find_all(class_="tab2")
    pass
def produce(classDic:dict):
    pass

# wC= parseScheme(rs)
# toJson=json.dumps(wC,ensure_ascii=False)
# with open("jsonrs.json","w",encoding="utf-8")as f:
#     f.write(toJson)

r=soup.find_all(class_='detail')
information=[]
for i in r:
    string=str()
    for x in i.stripped_strings:
        string+=x
    information.append(string)

print(information)
parseScheme(rs)
for i in information:
    if i!='':
        sourcels=i.split(' ')
        print(initInfo(sourcels))



