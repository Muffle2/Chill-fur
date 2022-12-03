import datetime, math, time


def now(mode):
	if mode == 0: return datetime.datetime.now().strftime("%H:%M:%S")
	if mode == 1: return datetime.datetime.now().strftime("%d/%m/%Y")
	if mode == 2: return datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
	if mode == 3: return math.trunc(time.time())