#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import json
from sseclient import SSEClient
import requests
import numpy as np
import random

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)
first = "\xF0\x9F\x94\xB4"
second = "\xF0\x9F\x9F\xA1"
def create_board():
    board = np.zeros((6, 7))
    return board
def makemove1(board,youAre,battleId,players,turn):
    rdata = {}
    if turn == 0 and youAre == first:

        rdata['action'] = 'putToken'
        rdata['column']  = "D"
        requests.post("https://cis2022-arena.herokuapp.com/connect4/play/" + battleId, data = rdata)
        rdata["player"] = youAre

    else:
        columns = "ABCDEFG"
        rdata['action'] = 'putToken'
        rdata['column']  = random.choice(columns)
        requests.post("https://cis2022-arena.herokuapp.com/connect4/play/" + battleId, data = rdata)
        rdata["player"] = youAre

    return rdata


def winning_move(board, piece):
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True
    return False



def updateBoard(board, data, youAre): # action of put token by both side
    col = data["column"]
    for i in range(6):
        if board[i][col] != 0:
            if data["player"] == youAre:
                board[i-1][col] = "X" # OUR MOVE
            else:
                board[i - 1][col] = "O"  # OPPONENT
            break
    else:
        board[5][col] = "O" #bottom of column
    return board


@app.route('/connect4', methods=['POST'])
def connect4():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    youAre = ""
    turn = 0
    gameOn = True
    board = create_board()
    while gameOn:
        url = 'https://cis2022-arena.herokuapp.com/connect4/start/'+battleId
        headers = {'Accept': 'text/event-stream'}
        messages = SSEClient(url) #get

        for msg in messages:
            data = msg.data
            logging.info("data sent from arena {}".format(data))
            if type(data) is str:
                try:
                    data = json.loads(data)
                except:
                    continue
            if "youAre" in data and turn ==0:    #initiate our position
                youAre = data["youAre"]
            # after initiated,
            # step by step: data: player(), action(), column
            # finals: winner()
            # flip: player(), action(flip)
            if data["action"] =="putToken":
                board = updateBoard(board,data, youAre)
                decision = makemove1(board,youAre,battleId,turn)
                board = updateBoard(board, decision, youAre)
            elif "winner" in data or "action" in data:
                break




            turn += 1
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