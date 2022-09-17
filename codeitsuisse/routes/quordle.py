import logging
import json

from flask import request, jsonify

from codeitsuisse import app
logger = logging.getLogger(__name__)

def check_uni_char(answers):
    unique_ans_char = "".join(set(answers))
    return unique_ans_char


@app.route('/quordleKeyboard', methods = ['POST'])
def quordle():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    real_alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    answers = data.get("answers")
    unique_ans_char = check_uni_char(answers)
    #print(unique_ans_char)
    attempts = data.get("attempts")
    greyed_out = {}
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for i in alphabet:
        if i not in greyed_out:
            greyed_out[i] = 0
    for attempt in attempts:
        for answer in answers:
            if attempt == answer:
                answers.remove(answer)
                unique_ans_char = check_uni_char(answers)       # check uni char remaining

        for attempt_letter in attempt:
            if attempt_letter in alphabet and attempt_letter not in unique_ans_char:
                for i in range(len(alphabet)):
                    if alphabet[i]  == attempt_letter:
                        alphabet[i] = " "
                        break
        for greyed_letter in greyed_out.keys():
            if greyed_letter not in alphabet:
                greyed_out[greyed_letter] += 1
        #print(attempt)
        #print(alphabet)
        #print(unique_ans_char)
        #for i in greyed_out.keys():
            #if greyed_out[i] > 0:
                #print(f'{i}:{greyed_out[i]}')
    result1 = ""
    for i in greyed_out.keys():
        if greyed_out[i] > 0:
            result1 += str(greyed_out[i])
    leftover = ""
    for i in alphabet:
        if i != " ":
            leftover += i
    print("leftover:", leftover)
    result2 = ""
    numbers = data.get("numbers")
    binary = []
    for number in numbers:
        if str(number) in  result1:
            binary.append(1)
        else:
            binary.append(0)
    for i in range(0,len(binary),5):
        bin = []
        for j in range(5):
            bin.append(str(binary[i+j]))
        bin = chr(int("".join(bin),2) + ord('A')-1)
        result2 += bin
    result2 += leftover










    result = {"part1": result1, "part2":result2}
    logging.info("My result :{}".format(result))
    return json.dumps(result)