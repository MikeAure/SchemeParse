import re



abbr_re=re.compile(r"\((\w+\d*)\)")
credit_re=re.compile(r"学分\[(\.?\d+\.?\d*)\]")
time_re=re.compile(r"时\[(\d+)\]")
teacher_re=re.compile("师\[(\w+,?\w*)\]")
room_re=re.compile(r"室\[(\w+-?\w*\d*,?\w*\d*)]")


def initInfo(classItem:list):
    className = classItem[0]
    rightnum = className.find(')')
    className = className[rightnum + 1:]
    abbr = abbr_re.findall(classItem[0])[0]
    rs = {}
    location = []
    teacherNames = []
    credit=float()
    totalTime = []
    for i in classItem:

        if time_re.search(i):
            time=time_re.findall(i)[0]
            totalTime.append(int(time))
        if teacher_re.search(i):
            teacher_name=teacher_re.findall(i)[0]
            teacherNames.append(teacher_name)
        if room_re.search(i):
            room=room_re.findall(i)[0]
            location.append(room)
        if credit_re.search(i):
            credit=float(credit_re.findall(i)[0])
            rs.update({'credit':credit})
    rs.update({'className':className,'totalTime':totalTime,'teacherNames':teacherNames,'location':location})
    return {abbr:rs}



