from bs4 import BeautifulSoup
import requests
import lxml
import json

class Class:
    def __init__(self):
        self.className=str()
        self.location=str()
        self.teacherName=str()
        self.goal=float()
        self.totalNum=int()
allClasses={}
# totalWeeks=input("Please input your total week number:")
# num=int()
# week=[{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''},{"1-2":'','3-4':'','5-6':'','7-8':'','9-11':''}]
# for i in range(int(totalWeeks)):
#     num=i+1
#     allClasses.update({num:week})

url="http://202.115.133.173:805/Classroom/ProductionSchedule/StuProductionSchedule.aspx"
header={'Cookie': 'ASP.NET_SessionId=v4x03ubilwsodb3ojpufvcfl; UserTokeID=d1c08ee9-6fb2-4c98-9f4c-2053e36c34d8'}
info={'termid':'202001','stuID':'201917030119'}
htmli=requests.get(url=url,params=info,headers=header)
rs=htmli.text

with open("result.html","w",encoding="utf-8") as f:
    f.write(rs)


soup=BeautifulSoup(open("result.html",encoding="utf-8"),"html.parser")
soup.prettify()
with open("result.html","w",encoding="utf-8") as f:
    f.write(str(soup))
rs=soup.find_all("tr")
for i in range(4):
    del rs[0]


# print(rs[0].contents)
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

        if tdItem["class"] == ["fontcss"]:
            if tdItem.has_attr("colspan") and tdItem["colspan"]=='12':
                continue
            else:
                if tdItem.has_attr("colspan"):
                    weekdayTemp=int(tdItem["colspan"])
                else:
                    weekdayTemp=1
                classContent=str()
                for content in tdItem.stripped_strings:
                    classContent=classContent+content+''
                if weekdayCal==0:
                    oneday.update({"1-2":classContent})
                    weekdayCal += weekdayTemp
                if weekdayCal==2:
                    oneday.update({"3-4":classContent})
                    weekdayCal += weekdayTemp
                if weekdayCal==5:
                    oneday.update({"5-6":classContent})
                    weekdayCal += weekdayTemp
                if weekdayCal==7:
                    oneday.update({"7-8":classContent})
                    weekdayCal += weekdayTemp
                if weekdayCal==9:
                    oneday.update({"9-11":classContent})
                    weekdayCal += weekdayTemp
                if weekdayCal==12:

                    currentWeek.append({weekday:oneday.copy()})
                    if weekday<=7:
                        weekday+=1
                    else:
                        weekday=1
                    weekdayCal=0
                    oneday.clear()
                    oneday.update({"1-2":classContent})

        wholeClasses[weekNum]=currentWeek

toJson=json.dumps(wholeClasses,ensure_ascii=False)
with open("jsonrs.json","w",encoding="utf-8")as f:
    f.write(toJson)
# while '\n' in lr:
#     lr.remove('\n')
# print(lr)



