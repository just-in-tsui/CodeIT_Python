import logging
import json

from flask import request, jsonify
from pwn import *

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/payload_stack', methods = ['GET'])
def paystack():
    target = process("./stack")
    target.send(2)
