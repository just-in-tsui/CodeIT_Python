#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import json
from sseclient import SSEClient
import requests
import random

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def flip(battleId):
    rdata = {}
    rdata['action'] = '(╯°□°)╯︵ ┻━┻'
    requests.post("https://cis2022-arena.herokuapp.com/connect4/play/" + battleId, data = rdata)
    print("flipped")

@app.route('/connect4', methods=['POST'])
def connect4():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    youAre = ""
    gameOn = True
    while gameOn:
        url = 'https://cis2022-arena.herokuapp.com/connect4/start/'+battleId
        headers = {'Accept': 'text/event-stream'}
        messages = SSEClient(url)
        for msg in messages:
            data = msg.data
            logging.info("data sent from arena {}".format(data))
            if type(data) is str:
                try:
                    data = json.loads(data)
                except:
                    continue
            try:
                print("making move")
                columns ="ABCDEFG"
                if "column" in data:
                    if data["column"] not in columns:
                    flip(battleId)
                    break
                if "player" in data:
                    if data['player'] != "\xF0\x9F\x94\xB4" and data['player'] != "\xF0\x9F\x9F\xA1":
                        flip(battleId)
                        break
                if "action" in data:
                    if data["action"] == '(╯°□°)╯︵ ┻━┻':
                        flip(battleId)
                        break
                else:
                    rdata = {}
                    rdata['action'] = 'putToken'
                    rdata['column'] = random.choice(columns)
                    requests.post("https://cis2022-arena.herokuapp.com/connect4/play/" + battleId, data = rdata)
                    continue
            except:
                print("Cant make move")
                try:
                    if(data['winner'] == "draw" or data['winner'] == youAre):
                        logging.info("Win game!")
                    else:
                        logging.info("Possibly lost game!")
                    gameOn = False
                    break
                except:
                    gameOn = False
                    break
    return json.dumps(data)

# def makemove2(board,youAre,battleId,players):
#     data = {}
#     data['action'] = "move"
#     data["position"] = ""
#     current_loc = int(players[0][1])
#     data["position"] = "e"+(current_loc+1)
#     players[0] = data["position"]
#     logging.info("My move :{}".format(data))
#     requests.post("https://cis2021-arena.herokuapp.com/quoridor/play/"+battleId, data = data)