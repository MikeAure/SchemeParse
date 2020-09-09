# coding=utf-8
import datetime
import json
import re
import pytz
import requests

first_day = datetime.date(2020, 9, 1)
add_one_day = datetime.timedelta(days=1)
cl = {'1-2': datetime.time(8, 10, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai')),
      '3-4': datetime.time(10, 15, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai')),
      '5-6': datetime.time(14, 30, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai')),
      '7-8': datetime.time(16, 25, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai')),
      '9-11': datetime.time(19, 10, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai')),
      }
delta_time = datetime.timedelta(minutes=95)

abbr_re = re.compile(r"\((\w+\d*)\)")
credit_re = re.compile(r"学分\[(\.?\d+\.?\d*)\]")
time_re = re.compile(r"时\[(\d+)\]")
teacher_re = re.compile("师\[(\w+,?\w*)\]")
room_re = re.compile(r"室\[(\w+-?\w*\d*,?\w*\d*)]")

start = datetime.date(2020, 9, 1)


class Class:
    def __init__(self, date_time, class_name, location, teacher_name, goal, total_num):
        self.Time = date_time
        self.className = class_name
        self.location = location
        self.teacherName = teacher_name
        self.goal = goal
        self.totalNum = total_num

    def display(self):
        print(self.Time, self.className, self.location, self.teacherName, self.goal, self.totalNum)


def login(Cookie: str, termid: str, stuID: str):
    url = "http://202.115.133.173:805/Classroom/ProductionSchedule/StuProductionSchedule.aspx"
    header = {'Cookie': Cookie}
    info = {'termid': termid, 'stuID': stuID}
    htmli = requests.get(url=url, params=info, headers=header)
    rs = htmli.text
    with open("result.html", "w", encoding="utf-8") as f:
        f.write(rs)
    return f


def judge(weekday_cal, oneday, weekday_temp, class_content, weekday, current_week):
    if weekday_cal == 2:
        oneday.update({"1-2": class_content})
    elif weekday_cal == 4:
        oneday.update({"3-4": class_content})
    elif weekday_cal == 7:
        oneday.update({"5-6": class_content})
    elif weekday_cal == 9:
        oneday.update({"7-8": class_content})
    elif (weekday_cal == 11 and class_content != '') or weekday_cal == 12:
        oneday.update({"9-11": class_content})
        current_week.update({weekday: oneday.copy()})
        if weekday <= 7:
            weekday += 1
            weekday_cal = 0
        oneday.clear()
        return (weekday_cal, weekday)

    return (weekday_cal, weekday)


def parseScheme(rs):
    wholeClasses = {}
    for tr in rs:
        lr = tr.find_all('td')  # tr块中所有td标签
        oneday = {}
        currentWeek = {}
        weekday = 1
        weekdayCal = 0
        for tdItem in lr:
            if tdItem["class"] == ['td1']:
                week_num = int(next(tdItem.stripped_strings)[0:-1])
                wholeClasses.update({week_num: []})
                continue

            if tdItem["class"] == ["fontcss"]:
                if tdItem.has_attr("colspan") and tdItem["colspan"] == '12':
                    weekday += 1
                    continue
                else:
                    if tdItem.has_attr("colspan"):
                        weekday_temp = int(tdItem["colspan"])
                    else:
                        weekday_temp = 1
                    class_content = str()
                    for content in tdItem.stripped_strings:
                        class_content = class_content + content + ' '
                    if class_content == "教研 ":
                        class_content = ''
                    weekdayCal += weekday_temp
                    (weekdayCal, weekday) = judge(weekdayCal, oneday, weekday_temp, class_content, weekday, currentWeek)

        wholeClasses[week_num] = currentWeek
    toJson = json.dumps(wholeClasses, ensure_ascii=False)
    with open("jsonrs.json", "w", encoding="utf-8")as f:
        f.write(toJson)
    return wholeClasses


def initInfo(classItem: list):
    class_name = classItem[0]
    rightnum = class_name.find(')')
    class_name = class_name[rightnum + 1:]
    abbr = abbr_re.findall(classItem[0])[0]
    rs = {}
    location = []
    teacherNames = []
    credit = float()
    totalTime = []
    for i in classItem:

        if time_re.search(i):
            time = time_re.findall(i)[0]
            totalTime.append(int(time))
        if teacher_re.search(i):
            teacher_name = teacher_re.findall(i)[0]
            teacherNames.append(teacher_name)
        if room_re.search(i):
            room = room_re.findall(i)[0]
            location.append(room)
        if credit_re.search(i):
            credit = float(credit_re.findall(i)[0])
            rs.update({'credit': credit})
    rs.update({'className': class_name, 'totalTime': totalTime, 'teacherNames': teacherNames, 'location': location})
    return {abbr: rs}


def dic2icslist(wholeClasses: dict, classesInfo: dict):
    result = []
    totalLoop = len(wholeClasses) + 1
    for i in range(1, totalLoop):
        temp = wholeClasses[i]
        for weekdaynum, classItem in temp.items():
            for classNum, classNameLs in classItem.items():
                if classNameLs != '' and classNameLs != '不排课 ':
                    increment = datetime.timedelta(days=((i - 1) * 7 + int(weekdaynum) - 2))
                    classHappen = datetime.datetime.combine(start + increment, cl[classNum],
                                                            tzinfo=pytz.timezone("Asia/Shanghai"))
                    classNameAbbr = classNameLs.split(' ')[0][0:-2]
                    classInfo = classesInfo[classNameAbbr]
                    className = classInfo['className']
                    teacherName = str()
                    for name in classInfo['teacherNames']:
                        teacherName += name + ' '
                    credit = classInfo['credit']
                    totalTime = str()
                    for time in classInfo['totalTime']:
                        totalTime += str(time) + ' '

                    location = classNameLs.split(' ')[1]
                    finalItem = Class(date_time=classHappen, class_name=className, teacher_name=teacherName, goal=credit,
                                      location=location, total_num=totalTime)
                    result.append(finalItem)
    return result
