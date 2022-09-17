#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import json
from sseclient import SSEClient
import requests

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe', methods=['POST'])
def tictactoe():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    board = ['NW','N','NE','W','C','E','SW','S','SE']
    played = ['','','','','','','','','']
    youAre = ""
    gameOn = True
    lastmove = ""
    while gameOn:
        flip = False
        url = 'https://cis2021-arena.herokuapp.com/tic-tac-toe/start/'+battleId
        headers = {'Accept': 'text/event-stream'}
        messages = SSEClient(url)
        for msg in messages:
            # r = requests.get('https://cis2021-arena.herokuapp.com/tic-tac-toe/start/'+battleId)
            data = msg.data
            logging.info("data sent from arena {}".format(data))
            # data = json.loads(msg.data.replace("'",'"'))
            if type(data) is str:
                try:
                    data = json.loads(data)
                except:
                    continue
            try:
                if( data['youAre'] != ""):
                    youAre = data['youAre']
                    if(data['youAre'] == "O"):
                        logging.info("Prepare to make move")
                        lastmove = makemove(board,played,youAre,battleId)
            except:
                try:
                    if(data['player'] == youAre):
                        if(data["position"] != lastmove):
                            flip = True
                            logging.info("Flip table")
                            gameOn = False
                            rdata = {}
                            rdata['action'] = '(╯°□°)╯︵ ┻━┻'
                            requests.post("https://cis2021-arena.herokuapp.com/tic-tac-toe/play/"+battleId, data = rdata)
                            break
                        continue
                    else:
                        try:
                            logging.info(played)
                            if(data['position'] not in board or played[board.index(data['position'])] != '' or data["action"] != "putSymbol"):
                                flip = True
                                logging.info("Flip table")
                                gameOn = False
                                rdata = {}
                                rdata['action'] = '(╯°□°)╯︵ ┻━┻'
                                requests.post("https://cis2021-arena.herokuapp.com/tic-tac-toe/play/"+battleId, data = rdata)
                                break
                            played[board.index(data['position'])] = data['player']
                            logging.info("Prepare to makemove")
                            lastmove = makemove(board,played,youAre,battleId)
                        except:
                            flip = True
                            logging.info("Flip table")
                            gameOn = False
                            rdata = {}
                            rdata['action'] = '(╯°□°)╯︵ ┻━┻'
                            requests.post("https://cis2021-arena.herokuapp.com/tic-tac-toe/play/"+battleId, data = rdata)
                            break
                except:
                    try:
                        if(data['winner'] == "draw" or data['winner'] == youAre):
                            logging.info("Win game !")
                        else:
                            logging.info("Possibly lost game !")
                        gameOn = False
                        break
                    except:
                        gameOn = False
                        break
        # if(flip):
        #     logging.info("Flip table")
        #     gameOn = False
        #     rdata = {}
        #     rdata['action'] = '(╯°□°)╯︵ ┻━┻'
        #     requests.post("https://cis2021-arena.herokuapp.com/tic-tac-toe/play/"+battleId, data = rdata)
        #     break
    return json.dumps(data)

def makemove(board,played,youAre,battleId):
    data = {}
    data['action'] = "putSymbol"
    data["position"] = ""
    if(played.count('') == 9):
        data["position"] = "NW"
        played[0] = youAre
    if(data["position"] == ""):
        for i in range(len(played)):
            if(played[i] == ''):
                temp = played[:]
                temp[i] = youAre
                if(checkwin(temp,youAre)):
                    played[i] = youAre
                    data["position"] = board[i]
                    break
    if(data["position"] == ""):
        if (youAre == "O"):
            opponent = "X"
        else:
            opponent = "O"
        for i in range(len(played)):
            if(played[i] == ''):
                temp = played[:]
                temp[i] = opponent
                if(checkwin(temp,opponent)):
                    played[i] = youAre
                    data["position"] = board[i]
                    break
    if(data["position"] == ""):
        if(played.count('') == 8):
            data["position"] = "C"
            played[4] = youAre
        elif(played.count('') == 7):
            if(played[4] != ''):
                data["position"] = "SE"
                played[8] = youAre
            else:
                if(played[1] != "" and played[2] != ""):
                    data["position"] = board[2]
                    played[2] = youAre
                elif(played[3] != "" and played[6] != ""):
                    data["position"] = board[6]
                    played[6] = youAre
                else:
                    data["position"] = "C"
                    played[4] = youAre
        else:
            for i in range(len(played)):
                if(played[i] == ''):
                    played[i] = youAre
                    data["position"] = board[i]
                    break
    logging.info("My move :{}".format(data))
    requests.post("https://cis2021-arena.herokuapp.com/tic-tac-toe/play/"+battleId, data = data)
    return data["position"]

def checkwin(played,youAre):
    if(played[0] == youAre and played[3] == youAre and played[6] == youAre):
        return True
    elif(played[1] == youAre and played[4] == youAre and played[7] == youAre):
        return True
    elif(played[2] == youAre and played[5] == youAre and played[8] == youAre):
        return True
    elif (played[0] == youAre and played[1] == youAre and played[2] == youAre):
        return True
    elif(played[3] == youAre and played[4] == youAre and played[5] == youAre):
        return True
    elif (played[6] == youAre and played[7] == youAre and played[8] == youAre):
        return True
    elif(played[0] == youAre and played[4] == youAre and played[8] == youAre):
        return True
    elif (played[2] == youAre and played[4] == youAre and played[6] == youAre):
        return True
    else:
        return False

def score(played,youAre):
    if youAre == 'O':
        opponent = 'X'
    else:
        opponent = 'O'
    if checkwin(played,youAre):
        return 10
    elif checkwin(played,opponent):
        return -10
    else:
        return 0

# def minimax(played,youAre):
#     if youAre == 'O':
#         opponent = 'X'
#     else:
#         opponent = 'O'
#     if checkwin(played,youAre) or checkwin(played,opponent):
#         return score(played,youAre)
#     scores = [] # an array of scores
#     moves = []  # an array of moves
#
#     # Populate the scores array, recursing as needed
#     for i in range(len(played)):
#         if(played[i] != ''):
#             temp = played[:]
#             temp[i] = youAre
#             scores.append(minimax(temp[i],youAre))
#             moves.append(i)
#
#     # Do the min or the max calculation
#     if game.active_turn == @player
#         # This is the max calculation
#         max_score_index = scores.each_with_index.max[1]
#         @choice = moves[max_score_index]
#         return scores[max_score_index]
#     else
#         # This is the min calculation
#         min_score_index = scores.each_with_index.min[1]
#         @choice = moves[min_score_index]
#         return scores[min_score_index]
#     end
# end
