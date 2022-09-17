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
    state = list(state)
    for day in days:
        date = datetime.date(year, 1, 1)  # Will give 1996-01-01
        delta = datetime.timedelta(day - 1)  # str(delta) will be '31 days, 0:00:00'
        newdate = date + delta  # date = 2022-03-21
        month_pos = newdate.month - 1
        dayOfWeek = newdate.weekday()  # Mon = 0 ,Sun = 6
        week = ["m", "t", "w", "t", "f", "s", "s"]
        if (month_pos == 11):
            print(day, newdate)
        if maxDays >= day > 0:
            state[month_pos * 8 + dayOfWeek] = week[dayOfWeek]
        if maxDays >= day > 0:
            new_days[month_pos].append(day)




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
    #print("STATE", "".join(state))

        #print("STATE", "".join(state))

    for i in range(12):
        if state[i * 8:i * 8 + 7] == ["m", "t", "w", "t", "f", " ", " "]:
            state[i * 8:i* 8 + 7] = ["w", "e", "e", "k", "d", "a", "y"]
        if state[i * 8:i * 8 + 7] == [" ", " ", " ", " ", " ", "s", "s"]:
            state[i * 8:i * 8 + 7] = ["w", "e", "e", "k", "e", "n", "d"]
        if state[i * 8:i * 8 + 7] == ["m", "t", "w", "t", "f", "s", "s"]:
            state[i * 8:i * 8 + 7] = ["a", "l", "l", "d", "a", "y", "s"]
    result1 = ''.join(state)
    print("~~~~", result1)
    # ------------------------------------
    index = result1.find(" ")
    newYear = 2001 + index
    input2 = result1.split(",")[:-1]
    #print(newYear,input2)

    weekends = []
    weekdays = []
    new_days = []
    for i in range(12):
        weekdays.append([])
        weekends.append([])
        new_days.append([])
    maxDays = checkLeapYear(newYear)  # check leap year
    for i in range(1, maxDays+1):
        date = datetime.date(newYear, 1, 1)  # Will give 1996-01-01
        delta = datetime.timedelta(i - 1)  # str(delta) will be '31 days, 0:00:00'
        newdate = date + delta  # date = 2022-03-21
        month_pos = newdate.month - 1  # month = 3 -> [2]
        if newdate.weekday() == 5 or newdate.weekday() == 6:
            weekends[month_pos].append(i)
            weekends[month_pos].sort()
        else:
            weekdays[month_pos].append(i)
            weekdays[month_pos].sort()
    for day in days:
        date = datetime.date(newYear, 1, 1)  # Will give 1996-01-01
        delta = datetime.timedelta(day - 1)  # str(delta) will be '31 days, 0:00:00'
        newdate = date + delta  # date = 2022-03-21
        month_pos = newdate.month - 1
        new_days[month_pos].append(day)
    result2 = [newYear]
    # Now we have all days ,weekdays, weekends sorted by month
    for month_pos in range(12):

        if input2[month_pos] == "alldays":
            alldays = weekdays[month_pos] + weekends[month_pos]
            result2.extend(alldays)
        elif input2[month_pos] == "weekday":
            result2.extend(weekdays[month_pos])
        elif input2[month_pos] == "weekend":
            result2.extend(weekends[month_pos])
        else:
            satisfied ={"Mo":False,"Tu": False, "We":False, "Th": False, "Fr":False, "Sa": False, "Su": False}
            #print(input2[month_pos])
            for j in weekdays[month_pos]: #checking every weekday in the month

                delta = datetime.timedelta(j - 1)  # str(delta) will be '31 days, 0:00:00'
                newdate = date + delta  # date = 2022-03-21
                if input2[month_pos][0] == 'm' and newdate.weekday() == 0 and not satisfied["Mo"]:
                    result2.append(j)
                    satisfied["Mo"] = True
                elif input2[month_pos][1] == 't' and newdate.weekday() == 1 and not satisfied["Tu"]:
                    result2.append(j)
                    satisfied["Tu"] = True
                elif input2[month_pos][2] == 'w' and newdate.weekday() == 2 and not satisfied["We"]:
                    result2.append(j)
                    satisfied["We"] = True
                elif input2[month_pos][3] == 't' and newdate.weekday() == 3 and not satisfied["Th"]:
                    result2.append(j)
                    satisfied["Th"] = True
                elif input2[month_pos][4] == 'f' and newdate.weekday() == 4 and not satisfied["Fr"]:
                    result2.append(j)
                    satisfied["Fr"] = True
            for j in weekends[month_pos]: #check every weekend
                delta = datetime.timedelta(j - 1)  # str(delta) will be '31 days, 0:00:00'
                newdate = date + delta  # date = 2022-03-21
                if input2[month_pos][5] == 's' and newdate.weekday() == 5 and not satisfied["Sa"]:
                    result2.append(j)
                    satisfied["Sa"] = True
                elif input2[month_pos][6] == 's' and newdate.weekday() == 6 and not satisfied["Su"]:
                    result2.append(j)
                    satisfied["Su"] = True

    print("***\n",year, result1, result2)







    result = {"part1": result1,"part2":result2}
    logging.info("part1 :{}".format(result))
    return json.dumps(result)


