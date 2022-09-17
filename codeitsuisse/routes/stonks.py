import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/stonks', methods = ['POST'])
def stonk():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    init_energy = data.get("energy")
    init_capital = data.get("capital")
    energy = init_energy
    capital = init_capital
    timeline = data.get("timeline")
    print(timeline)








    result = 1
    logging.info("My result :{}".format(result))
    return json.dumps(result)