import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/tickerStreamPart1', methods = ['POST'])
def ticker1():
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

@app.route('/tickerStreamPart2', methods = ['POST'])
def ticker2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    stream = data.get("stream")
    quantity_block = data.get("quantityBlock")
    data = []
    for stuffs in stream:
        ticks = stuffs.split(",")
        data.append(ticks)
    data.sort(key = lambda x: x[0])
    pairs = []
    cumu_list = {}
    for ticks in data:
        time = ticks[0]
        ticker = ticks[1]
        quantity = int(ticks[2])
        notion = round(float(ticks[3]), 1)
        original_floor = 0
        if ticker not in cumu_list:
            cumu_list[ticker] = [time, quantity, notion * quantity]
        else:  # Adding true q and n before applying q_block
            original_floor = cumu_list[ticker][1] // quantity_block  # if q=11, b=5, then of=2
            cumu_list[ticker][1] += quantity
            cumu_list[ticker][2] += quantity * notion
        new_floor = cumu_list[ticker][1] // quantity_block  # if q=16, b=5, then of=3
        if (new_floor != original_floor):
            adj_quantity = cumu_list[ticker][
                               1] // quantity_block * quantity_block
            adj_notion = cumu_list[ticker][2] - (cumu_list[ticker][1] %
                                                 quantity_block * notion)
            # use new floor (q = 15)

            pairs.append([time, ticker, adj_quantity, round(adj_notion, 1)])
    ret_dict = {}
    for i in pairs:
        time = i[0]
        if i[0] not in ret_dict:
            ret_dict[time] = [[i[1], i[2], i[3]]]
        else:
            ret_dict[time].append([i[1], i[2], i[3]])
        ret_dict[time].sort(key = lambda x: x[0])
    ret_list = []
    for i in ret_dict.keys():
        ret_str = f'{i},'
        for j in range(len(ret_dict[i])):
            if j != len(ret_dict[i]) - 1:
                for k in ret_dict[i][j]:
                    ret_str += f'{k},'
            else:
                for k in range(len(ret_dict[i][j])):
                    if k != len(ret_dict[i][j]) - 1:
                        ret_str += f'{ret_dict[i][j][k]},'
                    else:
                        ret_str += f'{ret_dict[i][j][k]}'
        ret_list.append(ret_str)
    logging.info("My result :{}".format(ret_list))
    result = { "output": ret_list}
    return json.dumps(result)