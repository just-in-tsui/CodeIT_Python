from collections import OrderedDict
import logging
import json
import pickle
from flask import request, jsonify
from codeitsuisse import app
logger = logging.getLogger(__name__)
@app.route("/instantiateDNSLookup", methods=["POST"])
@app.route("/ /instantiateDNSLookup", methods=["POST"])
def startDNS():
    with open("lookUp.json","w") as f:
        json.dump(request.get_json(),f)
    return jsonify({"success":True})
 
class LRUCache:
 
    # initialising capacity
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
 
    # we return the value of the key
    # that is queried in O(1) and return -1 if we
    # don't find the key in out dict / cache.
    # And also move the key to the end
    # to show that it was recently used.
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]
 
    # first, we add / update the key by conventional methods.
    # And also move the key to the end to show that it was recently used.
    # But here we will also check whether the length of our
    # ordered dictionary has exceeded our capacity,
    # If so we remove the first key (least recently used)
    def put(self, key: int, value: int) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)
 
@app.route("/simulateQuery",methods=["POST"])
@app.route("/ /simulateQuery",methods=["POST"])
def makeQuery():
    cache = LRUCache(request.get_json()['cacheSize'])
    print(cache.cache)
    output = []
    with open('lookUp.json') as f:
        dnsMap = (json.load(f))['lookupTable']
        logger.info(dnsMap)
    logger.info(request.get_json())
    for url in request.get_json()['log']:
        if url not in dnsMap:
            output.append({"status":"invalid",
            "ipAddress":"null"})
            continue
        if cache.get(url) != -1:
            output.append({"status":"cache hit",
            "ipAddress":cache.get(url)})
            continue
        output.append({"status":"cache miss",
            "ipAddress":dnsMap[url]})
        cache.put(url,dnsMap[url])
        
    return jsonify(output)

@app.route("/clearDNS",methods=["POST"])
def resetDNS():
    with open('lookUp.json', "w") as f:
        json.dump({"lookupTable":{}},f)
    return jsonify({"success":True})
        


 
 
