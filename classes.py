from bs4 import BeautifulSoup
from icalendar import *
from parse import *

def main():
    allClassesInfo={}

    soup=BeautifulSoup(open("./StuProductionSchedule.htm",encoding="utf-8"),"html.parser")
    soup.prettify()
    # with open("result.html","w",encoding="utf-8") as f:
    #     f.write(str(soup))
    rs=soup.find_all("tr")
    for i in range(4):
        del rs[0]

    r=soup.find_all(class_='detail')
    information=[]
    for i in r:
        string=str()
        for x in i.stripped_strings:
            string+=x
        information.append(string)
    wholeClasses=parseScheme(rs)
    for i in information:
        if i!='':
            sourcels=i.split(' ')
            allClassesInfo.update(initInfo(sourcels))

    schedule=dic2icslist(wholeClasses, allClassesInfo)

    cal=Calendar()
    cal.add('prodid', '-//Whitetree//whitetree.top//CN')
    cal.add('version', '2.0')
    cal.add('X-WR-CALNAME',{datetime.datetime.today()})
    cal.add('X-APPLE-CALENDAR-COLOR','#ff9500')
    cal.add('X-WR-TIMEZONE','Asia/Shanghai')
    for lesson in schedule:
        event=Event()
        event.add('summary',lesson.className)
        event.add('dtstart',lesson.Time)
        event.add('dtend',lesson.Time+delta_time)
        event.add('DESCRIPTION','授课教师：'+lesson.teacherName+'课时：'+lesson.totalNum+'学分：'+str(lesson.goal))
        event['location']=vText(lesson.location)
        alarm=Alarm()
        alarm.add('ACTION','DISPLAY')
        alarm.add('TRIGGER',datetime.timedelta(minutes=-10))
        alarm.add('DECRIPTION','上课提醒')
        event.add_component(alarm)
        cal.add_component(event)
    with open ('cal.ics','wb') as f:
        f.write(cal.to_ical())

if __name__=="__main__":
    main()
