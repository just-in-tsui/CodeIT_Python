import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/ticker1', methods = ['POST'])
def ticker():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")
    cumu_list = {}
    grouped_list = {}
    ret_list = []
    for data in stream:
        ticks = data.split(",")
        curr_time = ticks[0]
        if curr_time not in grouped_list:
            grouped_list[curr_time] = data[6:]
        else:
            grouped_list[curr_time] += f';{data[6:]}'
    grouped_list = sorted(grouped_list.items()
                          )  # A dict sorted by timestamp with ticks as values
    for i in grouped_list:
        ticks = i[1].split(";")
        ticks.sort(key = lambda x: x[0])  # sort ticker by alphabet
        ret = f'{i[0]},'
        for j in range(len(ticks)):
            tick = ticks[j]
            tick = tick.split(",")
            ticker = tick[0]
            quantity = int(tick[1])
            notion = round(float(tick[2]), 1)
            if ticker not in cumu_list:
                cumu_list[ticker] = [quantity, round(notion * quantity, 1)]
            else:
                cumu_list[ticker][0] += quantity
                cumu_list[ticker][1] += round(quantity * notion, 1)
            ret += f'{ticker},{cumu_list[ticker][0]},{round(cumu_list[ticker][1], 1)}'
            if j != len(ticks) - 1:
                ret += ","
        ret_list.append(f'{ret}')
    logging.info("My result :{}".format(ret_list))
    result = { "output": ret_list}
    return json.dumps(result)