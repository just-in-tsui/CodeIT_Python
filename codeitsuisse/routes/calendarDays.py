import logging
import json
import calendar, datetime

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)
def checkLeapYear(Year):
    if (Year % 400 == 0) and (Year % 100 == 0):
        return 366
    # not divided by 100 means not a century year
    # year divided by 4 is a leap year
    elif (Year % 4 == 0) and (Year % 100 != 0):
        return 366
    # if not divided by both 400 (century year) and 4 (not century year)
    # year is not leap year
    else:
        return 365


@app.route('/calendarDays', methods = ['POST'])
def cal():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("numbers")
    year = inputValue[0]
    maxDays = checkLeapYear(year)  # check leap year
    days = inputValue[1:]
    days.sort()
    state = ""
    for i in range(96):
        if i % 8 == 7:
            state += ","
        else:
            state += " "
    weekends = []
    weekdays = []
    new_days = []
    for i in range(12):
        weekdays.append([])
        weekends.append([])
        new_days.append([])

    for day in days:
        date = datetime.date(year, 1, 1)  # Will give 1996-01-01
        delta = datetime.timedelta(day - 1)  # str(delta) will be '31 days, 0:00:00'
        newdate = date + delta  # date = 2022-03-21
        month_pos = newdate.month - 1
        new_days[month_pos].append(day)
    state = list(state)
    for day in days:
        date = datetime.date(year, 1, 1)  # Will give 1996-01-01
        delta = datetime.timedelta(day - 1)  # str(delta) will be '31 days, 0:00:00'
        newdate = date + delta  # date = 2022-03-21
        # print(newdate)
        month_pos = newdate.month - 1  # month = 3 -> [2]
        dayOfWeek = newdate.weekday()  # Mon = 0 ,Sun = 6
        week = ["m", "t", "w", "t", "f", "s", "s"]
        # print(month_pos * 8 + dayOfWeek)

        state[month_pos * 8 + dayOfWeek] = week[dayOfWeek]
        print(state[month_pos * 8:month_pos * 8+6])
        if state[month_pos * 8:month_pos * 8+7] == ["m", "t", "w", "t", "f", " ", " "]:
            print("hello")
            state[month_pos * 8:month_pos * 8 + 7] = ["w", "e", "e", "k", "d", "a", "y"]

    for i in range(1, maxDays+1):
        date = datetime.date(year, 1, 1)  # Will give 1996-01-01
        delta = datetime.timedelta(i - 1)  # str(delta) will be '31 days, 0:00:00'
        newdate = date + delta  # date = 2022-03-21
        month_pos = newdate.month - 1  # month = 3 -> [2]
        if newdate.weekday() == 5 or newdate.weekday() == 6:
            weekends[month_pos].append(i)
            weekends[month_pos].sort()
        else:
            weekdays[month_pos].append(i)
            weekdays[month_pos].sort()

    for i in range(12):
        isWeekend = False
        isWeekday = False
        isAllWeekend = False
        isAllWeekday = False
        text1 = ["w", "e", "e", "k", "e", "n", "d"]
        text2 = ["w", "e", "e", "k", "d", "a", "y"]
        text3 = ["a", "l", "l", "d", "a", "y", "s"]

        if all(x in new_days[i] for x in weekends[i]):  # i = month -1
            isAllWeekend = True
        if all(x in new_days[i] for x in weekdays[i]):
            isAllWeekday = True
        for j in new_days[i]:
            if j in weekends[i]:
                isWeekend = True
            if j in weekdays[i]:
                isWeekday = True
        if isWeekend and not isWeekday:
            for j in range(7):
                state[8 * i + j] = text1[j]
        #if isWeekday and not isWeekend:
            #for j in range(7):
                #state[8 * i + j] = text2[j]
        if isAllWeekend and isAllWeekday:
            for j in range(7):
                state[8 * i + j] = text3[j]

    print(state)

    result = ''.join(state)
    result = {"part1": result,"part2": [2022,1]}
    logging.info("part1 :{}".format(result))
    return json.dumps(result)


