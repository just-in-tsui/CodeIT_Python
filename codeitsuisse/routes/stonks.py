import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

class stock:
    def __init__(self,name, ):
        self.name = name
        self.total_value = 0
        self.holding_quantity = 0





@app.route('/stonks', methods = ['POST'])
def stonk():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    init_energy = data.get("energy")
    init_capital = data.get("capital")
    basetime = 2037
    energy = init_energy
    capital = init_capital
    output = []
    portfolio = {}











    result = 1
    logging.info("My result :{}".format(result))
    return json.dumps(result)



