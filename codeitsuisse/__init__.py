from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.ticker
import codeitsuisse.routes.calendarDays
import codeitsuisse.routes.stonks
import codeitsuisse.routes.quordle



