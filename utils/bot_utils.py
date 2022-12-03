import os, random
from datetime import datetime
from utils.utils import readJSON, writeJSON


async def checkTIME():
	time = readJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
	if datetime.datetime.now().day in time["fecha"]:
		return True
	else:
		return False